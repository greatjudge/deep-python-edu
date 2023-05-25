import unittest
import cjson
import json

from random import choices
from faker import Faker


class TestLoads(unittest.TestCase):
    def test_empty_string(self):
        json_strs = ['', '  ', '\n  ']
        with self.subTest():
            for json_str in json_strs:
                with self.assertRaises(TypeError) as err:
                    cjson.loads(json_str)
                    self.assertEqual(str(err.exception),
                                     'Expected object or value')

    def test_empty_dict(self):
        json_strs = [
            '{}',
            '{   }',
            '  {   }  '
        ]
        with self.subTest():
            for json_str in json_strs:
                json_doc = json.loads(json_str)
                cjson_doc = cjson.loads(json_str)
                self.assertEqual(cjson_doc, json_doc)

    def test_simple(self):
        json_str = '{"hello": 10, "world": "value"}'
        json_doc = json.loads(json_str)
        cjson_doc = cjson.loads(json_str)
        self.assertEqual(cjson_doc, json_doc)

    def test_normal(self):
        json_strs = [
            '{    "key": "val"}',
            '{   "key" : 45 }',
            '{"key": 45.45}',
            '{    "key": "val"  , "key2": "val2"}',
            '{    "key": 67  , "key2": "val2", "key3": 78.989}',
            '{ "key1": "word1 word2", "key2": "word1 word2 word3"}',
            '{"up": "live", "rate": "war", "bring": "receive"}'
        ]
        with self.subTest():
            for json_str in json_strs:
                json_doc = json.loads(json_str)
                cjson_doc = cjson.loads(json_str)
                self.assertEqual(cjson_doc, json_doc)

    def test_dict_in_spaces(self):
        json_strs = [
            '  \n {    "key": "val"}  ',
            '  {   "key" : 45 }  ',
            '  {"key": 45.45}  ',
            '  {    "key": "val"  , "key2": "val2"}   ',
            '    {    "key": 67  , "key2": "val2", "key3": 78.989}  '
        ]
        with self.subTest():
            for json_str in json_strs:
                json_doc = json.loads(json_str)
                cjson_doc = cjson.loads(json_str)
                self.assertEqual(cjson_doc, json_doc)

    def test_invalid_json(self):
        json_strs = [
            '',
            '  ',
            '{ ',
            ' }',
            '{   "key" :  ks "fff" }',
            '{   "key" :   89, "fff" }',
            '{   "key" :   }',
            '{    "key" "val"}',
            '"key": "val"',
            '{"key": "val"'
        ]
        with self.subTest():
            for json_str in json_strs:
                with self.assertRaises(TypeError) as err:
                    cjson_doc = cjson.loads(json_str)
                    self.assertEqual(str(err.exception), 'Expected object or value')

    def test_generated_str(self):
        n, m = 1, 3
        faker = Faker()
        with self.subTest():
            for i in range(n):
                json_dct = {faker.word(): choices((faker.word(), 5654),
                                             weights=(90, 30))[0] for _ in range(m)}
                json_str = json.dumps(json_dct)
                self.assertEqual(cjson.loads(json_str),
                                 json_dct)


class TestDumps(unittest.TestCase):
    def test_empty(self):
        json_dict = {}
        self.assertEqual(json.dumps(json_dict), cjson.dumps(json_dict))

    def test_normal(self):
        json_dicts = [
            {'key1': 'value1'},
            {'key': 45},
            {'key': 65.344},
            {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'},
            {'key1': 'value1', 'key2': 45, 'key3': 'value3'},
            {'key1': 'value1', 'key2': 'value2', 'key3': 89.34}
        ]
        with self.subTest():
            for json_dict in json_dicts:
                self.assertEqual(cjson.dumps(json_dict),
                                 json.dumps(json_dict))

    def test_error_key(self):
        json_dicts = [
            {56: 'value'},
            {'key1': 'value1', (1, 2, 3): 'value2'}
        ]
        with self.subTest():
            for json_dict in json_dicts:
                with self.assertRaises(TypeError) as err:
                    cjson_str = cjson.dumps(json_dict)
                    self.assertEqual(str(err.exception), 'key must be str')

    def test_error_value(self):
        json_dicts = [
            {'key1': []},
            {'key1': 'value1', 'key2': (1, 2, 3)}
        ]
        with self.subTest():
            for json_dict in json_dicts:
                with self.assertRaises(TypeError) as err:
                    cjson_str = cjson.dumps(json_dict)
                    self.assertEqual(str(err.exception), 'value must be str or number')

    def test_generated_jsons(self):
        n, m = 5, 25
        faker = Faker()
        with self.subTest():
            for i in range(n):
                dct = {faker.word(): choices((faker.word(), 5654),
                                             weights=(90, 30))[0] for _ in range(m)}
                self.assertEqual(cjson.dumps(dct),
                                 json.dumps(dct))
