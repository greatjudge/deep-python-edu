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

EXECUTING = True


def signal_handler(signum, frame):
    global EXECUTING
    EXECUTING = False
    print('The shutdown has started')


signal.signal(signal.SIGINT, signal_handler)
# signal.signal(signal.SIGTERM, signal_handler)


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
    def __init__(self, work_queue: Queue[SocketType | ExitPill],
                 top_k: int, lock: Lock,
                 processed_urls: ProcessedURLs,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = work_queue
        self.top_k = top_k
        self.lock = lock
        self.processed_urls = processed_urls

    def run(self):
        while True:
            obj = self.queue.get()
            if isinstance(obj, ExitPill):
                break
            self._handle_connection(obj)
            obj.close()

    def _handle_connection(self, conn: SocketType):
        while True:
            try:
                data = conn.recv(1024)
            except socket.error as err:
                print('Error in connection socket recv!: ', err)
                break

            if not data:
                break
            url = data.decode()

            try:
                most_common = self._most_common_words(self._get_html(url),
                                                      self.top_k)
                message = json.dumps(most_common).encode()
            except requests.ConnectionError as err:
                message = json.dumps({'error': str(err)}).encode()
            except requests.Timeout:
                message = json.dumps({'error': 'request to url'
                                               ' exceeded 5 seconds'})
            conn.send(message)

            with self.lock:
                self.processed_urls.urls_count += 1
                print(f'Processed {self.processed_urls.urls_count} urls')

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
    def __init__(self, host=HOST, port=PORT):
        self.server = socket.create_server((host, port), reuse_port=True)
        self.handled_urls = ProcessedURLs()

    def run_server(self, num_workers: int, top_k: int):
        print('Starting server ...')
        self.server.listen(3)

        work_queue: Queue[SocketType | ExitPill] = Queue()
        lock = Lock()

        workers = [Worker(work_queue, top_k, lock, self.handled_urls)
                   for _ in range(num_workers)]

        for worker in workers:
            worker.start()

        print('Server is accepting connections')
        self.server.settimeout(1)
        while EXECUTING:
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


def main(num_workers: int, top_k: int):
    server = Server()
    server.run_server(num_workers, top_k)


if __name__ == '__main__':
    args = get_args()
    main(args.workers, args.top_k)
