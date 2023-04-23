import socket
import os

from argparse import ArgumentParser
from threading import Thread, Lock
from typing import TextIO


HOST = '127.0.0.1'
PORT = 8800


def get_args():
    descr = 'Отправляет запросы с урлами серверу по TCP'
    parser = ArgumentParser(description=descr)
    parser.add_argument('m', type=int, default=5, help='Количество потоков')
    parser.add_argument('filename', type=str, help='Имя файла с урлами')

    args = parser.parse_args()
    if not os.path.exists(args.filename):
        print(f'*** Usage error: {args.filename} does not exist')
    if args.m < 1:
        print('*** Usage error: m must be > 0')
    return parser.parse_args()


def work(urls_file: TextIO, addr: tuple[str, int], lock: Lock):
    try:
        conn = socket.create_connection(addr)
    except socket.error as err:
        print(f'Error in create_connection with {addr}: {err}')
        print('Stop the thread work')
        return

    with lock:
        line = urls_file.readline()
    while line:
        url = line.strip()

        try:
            conn.send(url.encode())
            data = conn.recv(2048)
        except socket.error as err:
            print(f'Error in communication with {addr}, {url=}!: {err}')
            break

        if data:
            print(f'{url}: {data.decode()}')

        with lock:
            line = urls_file.readline()
    conn.close()


def main(urls_filename: str, m_threads: int):
    with open(urls_filename, encoding='utf-8') as urls_file:
        lock = Lock()
        threads = [Thread(target=work, args=(urls_file, (HOST, PORT), lock))
                   for _ in range(m_threads)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


if __name__ == '__main__':
    args = get_args()
    main(args.filename, args.m)
