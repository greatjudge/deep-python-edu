import argparse
import sys
import socket
import json

from socket import SocketType
from threading import Thread, Lock
from queue import Queue
from collections import Counter

import requests
from bs4 import BeautifulSoup


HOST = '127.0.0.1'
PORT = 8800
urls_count = 0


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


def handle_url(url: str, top_k: int) -> bytes:
    res = requests.get(url)  # TODO Обработка ошибки

    # можно ли делегировать другому процессу?
    soup = BeautifulSoup(res.text, 'lxml')
    most_common = Counter(soup.get_text().split()).most_common(top_k)
    return json.dumps(dict(most_common)).encode()


def handle_connection(conn, top_k: int, lock: Lock):
    while True:
        data = conn.recv(1024)  # TODO Обработка ошибки
        if not data:
            break
        url = data.decode()
        message = handle_url(url, top_k)
        conn.send(message)

        with lock:
            global urls_count
            urls_count += 1
        print(f'Processed {urls_count} urls')


def thread_work(work_queue: Queue[SocketType], top_k: int, lock: Lock):
    while True:
        conn = work_queue.get()
        handle_connection(conn, top_k, lock)
        conn.close()


def main(num_workers: int, top_k: int):
    server = socket.create_server((HOST, PORT), reuse_port=True)
    server.listen(3)

    work_queue = Queue()
    lock = Lock()

    threads = [Thread(target=thread_work,
                      args=(work_queue, top_k, lock),
                      daemon=True)
               for _ in range(num_workers)]

    for thread in threads:
        thread.start()

    while True:
        conn, _ = server.accept()
        work_queue.put(conn)


if __name__ == '__main__':
    args = get_args()
    main(args.workers, args.top_k)
