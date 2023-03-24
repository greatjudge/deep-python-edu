import unittest
from unittest import mock

from parser import parse_json


class TestParser(unittest.TestCase):
    def test_parsing(self):
        json_str_obj = [
            ('{"key": "word"}',
             {'key': ['word']}),
            ('{"key": "word1 word2 word3"}',
             {'key': ['word1', 'word2', 'word3']}),
            ('{"key1": "word1 word2", "key2": "word2 word3"}',
             {'key1': ['word1', 'word2'],
              'key2': ['word2', 'word3']}),
            ('{"key1": "word1 word2", "key2": "word2 word3", "key3": "word2 word3 word4"}',
             {'key1': ['word1', 'word2'],
              'key2': ['word2', 'word3'],
              'key3': ['word2', 'word3', 'word4']})
        ]
        for string, obj in json_str_obj:
            with self.subTest():
                self.assertEqual(parse_json(string), obj)
                self.assertEqual(parse_json(string.replace('"', "'")), obj)

    def test_invalid_brackets(self):
        json_str = [
            '"key": "word"}',
            '{"key": "word"',
            '"key": "word"'
        ]
        for string in json_str:
            with self.subTest():
                with self.assertRaises(ValueError) as err:
                    parse_json(string)
                self.assertEqual(str(err.exception),
                                 'json_str should begins with { and ends with }')

    def test_invalid_quotation_marks_key(self):
        key_not_valid = [
            '{key: "word1 word2"}',
            '{"key: "word1 word2"}',
            '{key": "word1 word2"}',
            "{key: 'word1 word2'}",
            "{'key: 'word1 word2'}",
            "{key': 'word1 word2'}",
        ]

        for string in key_not_valid:
            with self.subTest():
                with self.assertRaises(ValueError) as err:
                    parse_json(string)
                self.assertEqual(str(err.exception),
                                 'key must end and begin with " or \'')

    def test_invalid_quotation_marks_words(self):
        words_not_valid = [
            '{"key": word1 word2}',
            '{"key": "word1 word2}',
            '{"key": word1 word2"}',
            "{'key': word1 word2}",
            "{'key': 'word1 word2}",
            "{'key': word1 word2'}"
        ]

        for string in words_not_valid:
            with self.subTest():
                with self.assertRaises(ValueError) as err:
                    parse_json(string)
                self.assertEqual(str(err.exception),
                                 'words must end and begin with " or \'')

    def test_callback(self):
        mock_keyword_callback = mock.Mock()
        mock_calls = []
        with self.subTest():
            simple_call = '{"key": "word1 word2 word3"}'
            json_obj = {'key': ['word1', 'word2', 'word3']}
            required_fields = ['key']
            keywords = ['word1']
            self.assertEqual(json_obj, parse_json(simple_call,
                                                  mock_keyword_callback,
                                                  required_fields,
                                                  keywords))
            mock_calls.append(mock.call(required_fields[0], keywords[0]))
            self.assertEqual(mock_calls,
                             mock_keyword_callback.mock_calls)

            several_keys = '{"key1": "word1 word2 only_key1",' \
                           ' "key2": "word1 word4",' \
                           ' "key3": "word1 word_hid only_key3"}'
            json_obj = {'key1': ['word1', 'word2', 'only_key1'],
                        'key2': ['word1', 'word4'],
                        'key3': ['word1', 'word_hid', 'only_key3']}
            required_fields = ['key1', 'key3']
            keywords = ['word1', 'only_key1', 'only_key3']
            self.assertEqual(json_obj, parse_json(several_keys,
                                                  mock_keyword_callback,
                                                  required_fields,
                                                  keywords))
            mock_calls.extend([mock.call('key1', 'word1'),
                               mock.call('key1', 'only_key1'),
                               mock.call('key3', 'word1'),
                               mock.call('key3', 'only_key3')])
            self.assertEqual(mock_calls,
                             mock_keyword_callback.mock_calls)
