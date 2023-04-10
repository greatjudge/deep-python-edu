import unittest
from lru_cashe import LRUCache


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
