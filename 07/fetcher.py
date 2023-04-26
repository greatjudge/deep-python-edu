import os
import asyncio
from argparse import ArgumentParser
from asyncio import Queue
from time import time

import aiohttp
from aiohttp import ClientSession, ClientResponse


Q_MAXSIZE = 50


def get_args():
    descr = 'Ассинхронно обкачивает урлы'
    parser = ArgumentParser(description=descr)
    parser.add_argument('-c', '--count_workers',
                        type=int, default=5,
                        help='Количество одновременных запросов')
    parser.add_argument('filename', type=str, help='Имя файла с урлами')

    args = parser.parse_args()
    if not os.path.exists(args.filename):
        print(f'*** Usage error: {args.filename} does not exist')
    if args.count_workers < 1:
        print('*** Usage error: -c --count_workers must be > 0')
    return parser.parse_args()


async def useful_action(res: ClientResponse):
    pass


async def fetch_url(url: str,
                    client: ClientSession) -> None:
    try:
        async with client.get(url, timeout=10) as res:
            print(f'{url} is fetched')
            await useful_action(res)
    except asyncio.TimeoutError as err:
        print(f'timeout error with url: {url}: {err}')


async def work(url_queue: Queue[str], client: ClientSession):
    while True:
        url = await url_queue.get()
        try:
            await fetch_url(url, client)
        finally:
            url_queue.task_done()


async def supervisor(filename: str, count_workers: int) -> None:
    url_queue = Queue(Q_MAXSIZE)
    with open(filename, encoding='utf-8') as file:
        async with aiohttp.ClientSession() as client:
            tasks = [asyncio.create_task(work(url_queue, client))
                     for _ in range(count_workers)]
            while line := file.readline():
                await url_queue.put(line.strip())
            await url_queue.join()
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)


def main(filename: str, count_workers: int):
    asyncio.run(supervisor(filename, count_workers))


if __name__ == '__main__':
    t0 = time()
    args = get_args()
    main(args.filename, args.count_workers)
    print(f'executing time: {time() - t0}')
