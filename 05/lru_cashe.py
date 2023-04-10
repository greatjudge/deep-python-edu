from typing import Any, Hashable, Optional
from dataclasses import dataclass


@dataclass
class Record:
    key: Optional[Hashable]
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

        self.records_dict = {}
        self.__limit = limit

        self.head = Record(key=None, value=None)
        self.tail = Record(key=None, value=None, prev=self.head)
        self.head.next = self.tail

    def get(self, key):
        record = self.records_dict.get(key)
        if record is None:
            return None
        self._move_to_start(record)
        return record.value

    def set(self, key, value):
        if len(self.records_dict) >= self.__limit:
            last_record = self.tail.prev
            if last_record is not self.head:
                del self.records_dict[last_record.key]
                self._delete_record(last_record)

        if key in self.records_dict:
            record = self.records_dict[key]
            record.value = value
            self._move_to_start(record)
        else:
            self.records_dict[key] = record = Record(key=key, value=value)
            self._append_start(record)

    def _append_start(self, record):
        record.prev, record.next = self.head, self.head.next
        self.head.next.prev = record
        self.head.next = record

    def _move_to_start(self, record):
        record.prev.next = record.next
        record.next.prev = record.prev

        record.prev, record.next = self.head, self.head.next
        self.head.next.prev = record
        self.head.next = record

    def _delete_record(self, record):
        if record is not self.head and record is not self.tail:
            record.prev.next, record.next.prev = record.next, record.prev
            del record
