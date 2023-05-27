import argparse
import signal
import sys
import socket
import json

from socket import SocketType
from threading import Thread, Lock
from queue import Queue
from collections import Counter
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


HOST = '127.0.0.1'
PORT = 8800


def signal_handler(signum, frame):
    Server.stop_all_servers()
    print('The shutdown has started')


signal.signal(signal.SIGINT, signal_handler)


def get_args():
    parser = argparse.ArgumentParser(description='TODO')
    parser.add_argument('-w', '--workers', type=int,
                        default=1, help='Число воркеров')
    parser.add_argument('-k', '--top_k', type=int,
                        default=5, help='Число самых частых слов')

    args = parser.parse_args()
    if args.workers < 1:
        print('*** Usage error: --workers must be >= 1')
        parser.print_usage()
        sys.exit(2)
    if args.top_k < 0:
        print('*** Usage error: --top_k must be >= 0')
        parser.print_usage()
        sys.exit(2)
    return args


@dataclass
class ProcessedURLs:
    urls_count: int = 0


class ExitPill:
    pass


class Worker(Thread):
    SOCKET_TIMEOUT = 10

    def __init__(self, work_queue: Queue[SocketType | ExitPill],
                 top_k: int, lock: Lock,
                 processed_urls: ProcessedURLs,
                 *args, **kwargs):
        """
        processed_urls: an object shared between threads
        """
        super().__init__(*args, **kwargs)
        self.queue = work_queue
        self.top_k = top_k
        self.lock = lock
        self.processed_urls = processed_urls

    def run(self):
        while True:
            try:
                obj = self.queue.get()
                if isinstance(obj, ExitPill):
                    break
                obj.settimeout(self.SOCKET_TIMEOUT)
                self._handle_connection(obj)
                obj.close()
            except Exception as err:
                print(err)

    def _handle_connection(self, conn: SocketType):
        while True:
            try:
                try:
                    data = conn.recv(2048)
                except socket.timeout as err:
                    mes = f'the waiting time {self.SOCKET_TIMEOUT}s' \
                          f' was exceeded: {err}'
                    conn.send(mes.encode())
                    break
                except socket.error as err:
                    print('Error in connection socket recv!: ', err)
                    continue

                if not data:
                    break
                url = data.decode()

                try:
                    most_common = self._most_common_words(self._get_html(url),
                                                          self.top_k)
                    message = json.dumps(most_common).encode()
                except requests.ConnectionError as err:
                    message = json.dumps({'error': str(err)}).encode()
                except requests.exceptions.MissingSchema as err:
                    message = json.dumps({'error': f'invalid url:'
                                                   f' {err}'}).encode()
                except requests.Timeout:
                    message = json.dumps({'error': 'request to url'
                                                   ' exceeded 5 seconds'})
                conn.send(message)

                with self.lock:
                    self.processed_urls.urls_count += 1
                    print(f'Processed {self.processed_urls.urls_count} urls')
            except Exception as err:
                print(err)

    @staticmethod
    def _most_common_words(text: str, top_k: int) -> dict[str, int]:
        soup = BeautifulSoup(text, 'lxml')
        words = soup.get_text().split()
        return dict(Counter(words).most_common(top_k))

    @staticmethod
    def _get_html(url: str) -> str:
        res = requests.get(url, timeout=5)
        return res.text


class Server:
    EXECUTING_ALL = True

    def __init__(self, host=HOST, port=PORT):
        self.server = socket.create_server((host, port), reuse_port=True)
        self.executing = True
        self.processed_urls = ProcessedURLs()

    @classmethod
    def stop_all_servers(cls):
        cls.EXECUTING_ALL = False

    @classmethod
    def allow_servers_to_execute(cls):
        cls.EXECUTING_ALL = True

    def stop_server(self):
        """
        called from another thread
        """
        self.executing = False

    def is_running(self) -> bool:
        return self.__class__.EXECUTING_ALL and self.executing

    def run_server(self, num_workers: int, top_k: int):
        self.executing = True
        if not self.EXECUTING_ALL:
            print('instances are not allowed to execute',
                  'call "allow_servers_to_execute" before run')
        print('Starting server ...')
        self.server.listen(3)

        work_queue: Queue[SocketType | ExitPill] = Queue()
        lock = Lock()

        workers = [Worker(work_queue, top_k, lock, self.processed_urls)
                   for _ in range(num_workers)]

        for worker in workers:
            worker.start()

        print('Server is accepting connections')
        self.server.settimeout(1)
        while self.is_running():
            try:
                conn, _ = self.server.accept()
                work_queue.put(conn)
            except socket.timeout:
                continue

        print('Server doesnt accept new connections')
        print('Processing existing connections ...')

        exit_pill = ExitPill()
        for _ in range(num_workers):
            work_queue.put(exit_pill)

        for worker in workers:
            worker.join()

        print('Shutdown')
        self.server.close()


def run_server(num_workers: int, top_k: int):
    server = Server()
    server.run_server(num_workers, top_k)


if __name__ == '__main__':
    args = get_args()
    run_server(args.workers, args.top_k)
