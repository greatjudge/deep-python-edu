import unittest
import cjson
import json


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
            '{    "key": 67  , "key2": "val2", "key3": 78.989}'
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

