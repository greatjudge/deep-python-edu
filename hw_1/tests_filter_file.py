import unittest
from io import StringIO
from filter_file import gen_filtered_string


class TestFilteredString(unittest.TestCase):
    def test_without_filtering(self):
        strings = [
            'first string',
            'second string',
            'third string',
            'fourth string'
        ]
        fp = StringIO('\n'.join(strings))
        self.assertEqual([],
                         list(gen_filtered_string(fp)))

    def test_filter_one_str(self):
        words = ['word']
        strings = [
            'first string klkl',
            'fdfsd klkd word dfd',
            'ldxd ldlf lfdl lcd',
        ]
        result = ['fdfsd klkd word dfd\n']
        fp = StringIO('\n'.join(strings))
        self.assertEqual(result,
                         list(gen_filtered_string(fp, words)))

    def test_case_independent(self):
        words = ['WoRd']
        strings = [
            'normal word',
            'all large WORD',
            'without klklmk sadff',
            'chaotic WOrD',
            'excatly WoRd',
            'small word',
        ]
        result = [
            'normal word\n',
            'all large WORD\n',
            'chaotic WOrD\n',
            'excatly WoRd\n',
            'small word',
        ]
        fp = StringIO('\n'.join(strings))
        self.assertEqual(result,
                         list(gen_filtered_string(fp, words)))

    def test_empty_result(self):
        words = ['word']
        strings = [
            'first string',
            'second string',
            'last string',
        ]
        fp = StringIO('\n'.join(strings))
        self.assertEqual([],
                         list(gen_filtered_string(fp, words)))

    def test_full_word_match(self):
        words = ['word']
        strings = [
            'second lower symb wor',
            'first full word',
            'third prefix of another wordsuffix',
            'fourth suffix of another prefixword',
            'last word full',
        ]
        result = [
            'first full word\n',
            'last word full',
        ]
        fp = StringIO('\n'.join(strings))
        self.assertEqual(result,
                         list(gen_filtered_string(fp, words)))

    def test_several_words(self):
        words = ['word-1', 'word-2', 'word-3']
        strings = [
            'conteins only one word-1\n',
            'kdlfkvfbl\n',
            'conteins only one word-2\n',
            'just string lkfdlk\n',
            'conteins only one word-3\n',
            'conteins two word-1 and word-2\n',
            'conteins three word-1 hhjhi word-2, and word-3 in the end\n',
            'no one',
        ]
        result = [
            'conteins only one word-1\n',
            'conteins only one word-2\n',
            'conteins only one word-3\n',
            'conteins two word-1 and word-2\n',
            'conteins three word-1 hhjhi word-2, and word-3 in the end\n',
        ]
        fp = StringIO('\n'.join(strings))
        self.assertEqual(result,
                         list(gen_filtered_string(fp, words)))

