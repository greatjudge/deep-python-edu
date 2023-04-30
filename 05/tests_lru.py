import unittest
from lru_cashe import LRUCache
from random import randrange


class LRUTest(unittest.TestCase):
    def test_normal(self):
        cache = LRUCache()
        items_diff_keys = [('key1', 'value1'), ('key2', 'value2'),
                           ('key', 'value'), ('key3', 'value1')]
        with self.subTest():
            for key, value in items_diff_keys:
                self.assertIsNone(cache.get(key))
                cache.set(key, value)
                self.assertEqual(cache.get(key), value)

    def test_reset(self):
        cache = LRUCache()
        self.assertIsNone(cache.get('key'))

        cache.set('key', 'value')
        self.assertEqual(cache.get('key'), 'value')

        cache.set('key', 'another value')
        self.assertEqual(cache.get('key'), 'another value')

    def test_limit(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertIsNone(cache.get('k3'))
        self.assertEqual(cache.get('k2'), 'val2')
        self.assertEqual(cache.get('k1'), 'val1')

        cache.set('k3', 'val3')

        self.assertEqual(cache.get('k3'), 'val3')
        self.assertIsNone(cache.get('k2'))
        self.assertEqual(cache.get('k1'), 'val1')

    def test_one_elem(self):
        cache = LRUCache(1)

        self.assertIsNone(cache.get('key'))
        cache.set('key', 'value')
        self.assertEqual(cache.get('key'), 'value')
        cache.set('key', 'another value')
        self.assertEqual(cache.get('key'), 'another value')

        self.assertIsNone(cache.get('key1'))
        cache.set('key1', 'value1')
        self.assertIsNone(cache.get('key'))
        self.assertEqual(cache.get('key1'), 'value1')

    def test_insert_update_displacement(self):
        limit = 10
        cache = LRUCache(limit)

        # insert
        for i in range(limit):
            key, value = f'key_{i}', f'value_{i}'
            self.assertIsNone(cache.get(key))
            cache.set(key, value)
            self.assertEqual(cache.get(key), value)

        # update
        i_isnot_update = randrange(limit)
        not_update_key = f'key_{i_isnot_update}'
        for i in range(limit):
            if i != i_isnot_update:
                key, new_value = f'key_{i}', f'new_value_{i}'
                cache.set(key, new_value)
                self.assertEqual(cache.get(key), new_value)

        # insert new
        new_key, value = 'new_key', 'new_key_value'
        self.assertIsNone(cache.get(new_key))
        cache.set(new_key, value)
        self.assertEqual(cache.get(new_key), value)

        # not_update_key is displaced
        self.assertIsNone(cache.get(not_update_key))

        # updated keys is not displaced
        for i in range(limit):
            if i != i_isnot_update:
                key, new_value = f'key_{i}', f'new_value_{i}'
                self.assertEqual(cache.get(key), new_value)

    def test_reached_limit_update_key(self):
        limit = 10
        cache = LRUCache(limit)
        for i in range(limit):
            key, value = f'key_{i}', f'value_{i}'
            self.assertIsNone(cache.get(key))
            cache.set(key, value)
            self.assertEqual(cache.get(key), value)
        key, new_value = f'key_{limit - 1}', f'new_value_{limit - 1}'
        cache.set(key, new_value)
        self.assertEqual(cache.get(key), new_value)

        for i in range(limit - 1):
            key, value = f'key_{i}', f'value_{i}'
            self.assertEqual(cache.get(key), value)

