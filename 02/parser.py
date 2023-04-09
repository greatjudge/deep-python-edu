"""
json parser
"""
import json

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
    callback_condition = all((keyword_callback is not None,
                              required_fields is not None,
                              keywords is not None))
    if callback_condition:
        required_fields_set = set(required_fields)
        keywords_set = set(keywords)

    json_obj = json.loads(json_str)
    for key, words in json_obj.items():
        if callback_condition and key in required_fields_set:
            words_list = words.split(' ')
            for word in words_list:
                if word in keywords_set:
                    keyword_callback(key, word)
        json_obj[key] = words
    return json_obj
