from typing import Any, Hashable
from dataclasses import dataclass


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


class LRUCache:

    def __init__(self, limit=42):
        if limit <= 0:
            raise ValueError(f'limit must be > 0, not {limit}')

        self.records_dict: dict[Hashable, Record] = {}
        self.__limit = limit

        self.head = Record(key=None, value=None)
        self.tail = Record(key=None, value=None, prev=self.head)
        self.head.next = self.tail

    def get(self, key):
        if key not in self.records_dict:
            return None
        record = self.records_dict[key]
        self._move_to_start(record)
        return record.value

    def set(self, key, value):
        if key in self.records_dict:
            record = self.records_dict[key]
            record.value = value
            self._move_to_start(record)
        else:
            if len(self.records_dict) >= self.__limit:
                last_record = self.tail.prev
                # there is no check that last_record is head because limit > 0
                self._remove_from_dll(last_record)
                del self.records_dict[last_record.key]
                del last_record
            self.records_dict[key] = record = Record(key=key, value=value)
            self._insert_after(self.head, record)

    def _move_to_start(self, record):
        self._remove_from_dll(record)
        self._insert_after(self.head, record)

    @staticmethod
    def _remove_from_dll(record: Record):
        record.prev.next = record.next
        record.next.prev = record.prev

    @staticmethod
    def _insert_after(after_which: Record, record: Record):
        record.prev, record.next = after_which, after_which.next
        after_which.next.prev = record
        after_which.next = record
