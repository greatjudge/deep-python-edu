from pathlib import Path
from time import perf_counter
from zipfile import ZipFile

import json
import cjson
import ujson


def ujson_dumps(jsons_directory: Path):
    all_time = 0
    for filename in jsons_directory.glob('*.json'):
        with open(filename) as file:
            json_dct = ujson.load(file)

            t0 = perf_counter()
            ujson_str = ujson.dumps(json_dct)
            all_time += perf_counter() - t0
    return all_time


def json_dumps(jsons_directory: Path):
    all_time = 0
    for filename in jsons_directory.glob('*.json'):
        with open(filename) as file:
            json_dct = ujson.load(file)

            t0 = perf_counter()
            json_str = json.dumps(json_dct)
            all_time += perf_counter() - t0
    return all_time


def cjson_dumps(jsons_directory: Path):
    all_time = 0
    for filename in jsons_directory.glob('*.json'):
        with open(filename) as file:
            json_dct = ujson.load(file)

            t0 = perf_counter()
            cjson_dct = cjson.dumps(json_dct)
            all_time += perf_counter() - t0
    return all_time


def ujson_loads(jsons_directory: Path):
    all_time = 0
    for filename in jsons_directory.glob('*.json'):
        with open(filename) as file:
            json_str = file.read()

            t0 = perf_counter()
            ujson_dct = ujson.loads(json_str)
            all_time += perf_counter() - t0
    return all_time


def json_loads(jsons_directory: Path):
    all_time = 0
    for filename in jsons_directory.glob('*.json'):
        with open(filename) as file:
            json_str = file.read()

            t0 = perf_counter()
            json_dct = json.loads(json_str)
            all_time += perf_counter() - t0
    return all_time


def cjson_loads(jsons_directory: Path):
    all_time = 0
    for filename in jsons_directory.glob('*.json'):
        with open(filename) as file:
            json_str = file.read()
            json_dict = json.loads(json_str)

            t0 = perf_counter()
            cjson_dct = cjson.loads(json_str)
            all_time += perf_counter() - t0
            assert cjson_dct == json_dict
    return all_time


def main():
    with ZipFile('jsons.zip') as myzip:
        myzip.extractall()
    jsons_directory = Path('jsons')

    cjson_time = cjson_loads(jsons_directory)
    json_time = json_loads(jsons_directory)
    ujson_time = ujson_loads(jsons_directory)
    print('perfomance loads')
    print(f'cjson_time: {cjson_time}')
    print(f'json_time: {json_time}')
    print(f'ujson_time: {ujson_time}')
    print()

    cjson_time = cjson_dumps(jsons_directory)
    json_time = json_dumps(jsons_directory)
    ujson_time = ujson_dumps(jsons_directory)
    print('perfomance dumps')
    print(f'cjson_time: {cjson_time}')
    print(f'json_time: {json_time}')
    print(f'ujson_time: {ujson_time}')
    print()


if __name__ == '__main__':
    main()
