"""
json parser
"""
from typing import Iterable, Optional
from collections.abc import Callable


def parse_json(json_str: str,
               keyword_callback: Optional[Callable[[str, str], ...]] = None,
               required_fields: Optional[Iterable[str]] = None,
               keywords: Optional[Iterable[str]] = None) -> dict:
    """
    Parse json string specific format
     and keyword_callback for key from required_fields and words from keywords
    :param json_str: format '{"key1": "Word1 word2", "key2": "word2 word3"}'
    :param keyword_callback: function(key, word)
    :param required_fields: keys for which  keyword_callback is called
    :param keywords: words for which  keyword_callback is called
    :return: json_obj (dict)
    """
    if json_str[0] != '{' or json_str[-1] != '}':
        raise ValueError('json_str should begins with { and ends with }')

    keyword_callback_condition = (
            keyword_callback is not None and
            required_fields is not None and
            keywords is not None
    )

    if keyword_callback_condition:
        required_fields_set = set(required_fields)
        keywords_set = set(keywords)

    json_obj = {}
    for key_words in json_str.strip('{}').split(','):
        key, words = key_words.split(':')
        key, words = key.strip(), words.strip()

        if (key[0], key[-1]) not in (('"', '"'), ("'", "'")):
            raise ValueError('key must end and begin with " or \'')
        if (words[0], words[-1]) not in (('"', '"'), ("'", "'")):
            raise ValueError('words must end and begin with " or \'')

        key, words_list = key.strip('"\''), words.strip('" \'').split(' ')

        if key in json_obj:
            raise ValueError('keys in  json_str must be unique')
        json_obj[key] = []

        for word in words_list:
            json_obj[key].append(word)

            if (
                    keyword_callback_condition and
                    key in required_fields_set and
                    word in keywords_set
            ):
                keyword_callback(key, word)
    return json_obj
