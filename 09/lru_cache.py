import logging

from typing import Any, Hashable
from dataclasses import dataclass
from argparse import ArgumentParser


class Filter(logging.Filter):
    def filter(self, record):
        return len(record.msg.split()) % 2 == 0


def get_logger():
    format_file = logging.Formatter("%(asctime)s\t%(levelname)s\t"
                                    "[file]\t%(message)s")
    loglru_handler = logging.FileHandler('lru_cache.log')
    loglru_handler.setLevel(logging.DEBUG)
    loglru_handler.setFormatter(format_file)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(loglru_handler)
    return logger


def get_args():
    parser = ArgumentParser()
    parser.add_argument('-s', action='store_true',
                        help='Доп логирование в stdout')
    parser.add_argument('-f', action='store_true',
                        help='Применение фильтра')
    return parser.parse_args()


@dataclass
class Record:
    key: Hashable | None
    value: Any
    prev: Any = None
    next: Any = None

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key


logger = get_logger()


class LRUCache:

    def __init__(self, limit: int = 42):
        if limit <= 0:
            logger.error('init limit with %d <= 0', limit)
            raise ValueError(f'limit must be > 0, not {limit}')

        self.records_dict: dict[Hashable, Record] = {}
        self.__limit = limit

        self.head = Record(key=None, value=None)
        self.tail = Record(key=None, value=None, prev=self.head)
        self.head.next = self.tail

    def get(self, key):
        if key not in self.records_dict:
            logger.warning('get non-existing key %s', key)
            return None
        logger.info('get existing key %s', key)
        record = self.records_dict[key]
        self._move_to_start(record)
        return record.value

    def set(self, key, value):
        if key in self.records_dict:
            logger.info('set existing key %s', key)
            record = self.records_dict[key]
            record.value = value
            self._move_to_start(record)
        else:
            if len(self.records_dict) >= self.__limit:
                logger.error('set the missing key %s'
                             ' when the capacity is reached', key)
                last_record = self.tail.prev
                # there is no check that last_record is head because limit > 0
                self._remove_from_dll(last_record)
                del self.records_dict[last_record.key]
                del last_record
            else:
                logger.info('set the missing key %s', key)
            self.records_dict[key] = record = Record(key=key, value=value)
            self._insert_after(self.head, record)

    def _move_to_start(self, record):
        logger.debug('move record to start, key %s', record.key)
        self._remove_from_dll(record)
        self._insert_after(self.head, record)

    @staticmethod
    def _remove_from_dll(record: Record):
        logger.debug('remove from dll , key %s', record.key)
        record.prev.next = record.next
        record.next.prev = record.prev

    @staticmethod
    def _insert_after(after_which: Record, record: Record):
        logger.debug('insert %s after %s', record.key, after_which.key)
        record.prev, record.next = after_which, after_which.next
        after_which.next.prev = record
        after_which.next = record


if __name__ == '__main__':
    args = get_args()
    if args.s:
        format_stream = logging.Formatter("%(asctime)s\t%(levelname)s\t"
                                          "[stream]\t%(message)s")
        stream = logging.StreamHandler()
        stream.setFormatter(format_stream)
        logger.addHandler(stream)
    if args.f:
        logger.addFilter(Filter())
    cache = LRUCache(3)
    # logger.setLevel(logging.DEBUG)

    cache.get('non_ex_key')
    cache.set('key', 'value')
    cache.get('key')
    cache.set('key2', 'value')
    cache.set('key3', 'value')
    cache.set('key2', 'value')
    cache.set('key4', 'value')
    cache.set('key3', 'value2')
