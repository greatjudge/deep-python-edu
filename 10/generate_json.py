import json
from random import choices
from argparse import ArgumentParser

from faker import Faker


def get_args():
    descr = 'Генерирует n json-файлов размера m'
    parser = ArgumentParser(description=descr)
    parser.add_argument('n', type=int, help='Количество json файлов')
    parser.add_argument('m', type=int, default=1000, help='Размер одного json файла')
    return parser.parse_args()


def generate_json(m: int, filename: str):
    faker = Faker()
    dct = {faker.word(): choices((faker.word(), 5654), weights=(90, 30))[0] for _ in range(m)}
    with open(filename, 'w') as file:
        json.dump(dct, file)


def main(n: int, m: int):
    for i in range(n):
        generate_json(m, f'jsons/json-{i}.json')


if __name__ == '__main__':
    args = get_args()
    main(args.n, args.m)
