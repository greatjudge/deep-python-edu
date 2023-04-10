from typing import Any
from dataclasses import dataclass


@dataclass
class Record:
    key: Any
    value: Any
    prev: Any = None
    next: Any = None

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key


class LRUCache:

    def __init__(self, limit=42):
        self.records_dict = {}
        self.limit = limit

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
        if len(self.records_dict) >= self.limit:
            last_record = self.tail.prev
            if last_record is not self.head:
                del self.records_dict[last_record.key]
                self._delete_rec(last_record)

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

    def _delete_rec(self, record):
        record.prev.next = self.tail
        self.tail.prev = record.prev
