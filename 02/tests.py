import json
import unittest

from unittest import mock
from random import randint, choices
from faker import Faker

from parser import parse_json

unittest.util._MAX_LENGTH=2000


class TestParser(unittest.TestCase):
    def test_parsing(self):
        mock_keyword_callback = mock.Mock()
        mock_calls = []
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
        with self.subTest():
            for string, obj in json_str_obj:
                self.assertEqual(parse_json(string, mock_keyword_callback), obj)
                self.assertEqual(mock_calls,
                                 mock_keyword_callback.mock_calls)

                self.assertEqual(parse_json(string, mock_keyword_callback, [], []), obj)
                self.assertEqual(mock_calls,
                                 mock_keyword_callback.mock_calls)

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

    def test_random_words(self):
        faker = Faker(locale="Ru_ru")

        for i in range(20):
            mock_keyword_callback = mock.Mock()
            mock_calls = []

            keywords = [faker.word() for _ in range(randint(1, 20))]
            keys = list(set([faker.word() for _ in range(randint(1, 20))]))
            required_keys = choices(keys, k=randint(0, len(keys)))

            json_obj = {}
            json_obj_to_func = {}
            for key in keys:
                kwords = choices(keywords, k=randint(0, len(keywords)))
                if key in required_keys:
                    mock_calls.extend([mock.call(key, word) for word in kwords])
                all_words = kwords + list(filter(lambda w: w not in keywords,
                                                 (faker.word() for _ in range(randint(1, 20)))))
                json_obj_to_func[key] = ' '.join(all_words)
                json_obj[key] = all_words
            json_str = json.dumps(json_obj_to_func, ensure_ascii=False)

            self.assertEqual(json_obj, parse_json(json_str,
                                                  mock_keyword_callback,
                                                  required_keys,
                                                  keywords))
            self.assertCountEqual(mock_calls, mock_keyword_callback.mock_calls)

