import os
import asyncio
from argparse import ArgumentParser

import aiohttp
from aiohttp import ClientSession, ClientResponse


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


async def useful_actoin(res: ClientResponse):
    pass


async def fetch_content(url: str, client: ClientSession):
    try:
        async with client.get(url, timeout=5) as res:
            await useful_actoin(res)
            print(f'{url} is fetched')
    except asyncio.TimeoutError as err:
        print(f'timeout error in url: {url}: {err}')


async def supervisor(filename: str, count_workers: int):
    semaphore = asyncio.Semaphore(count_workers)
    with open(filename, encoding='utf-8') as file:
        async with aiohttp.ClientSession() as client:
            while line := file.readline():
                url = line.strip()
                async with semaphore:
                    await fetch_content(url, client)


def main(filename: str, count_workers: int):
    asyncio.run(supervisor(filename, count_workers))


if __name__ == '__main__':
    args = get_args()
    main(args.filename, args.count_workers)
