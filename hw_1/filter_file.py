"""
filter lines in file
"""
from typing import Iterable, TextIO, Optional


def gen_filtered_string(fileobj: Optional[TextIO],
                        words: Optional[Iterable[str]] = ()):
    words_set = set(map(str.lower, words))
    for line in fileobj:
        if words_set \
              and set(line.strip().lower().split(' ')).intersection(words_set):
            yield line


# if __name__ == '__main__':
#     with open('text_file.txt', 'r') as file:
#         for s in gen_filtered_string(file,
#                                      ['роза', 'подсолнух']):
#             print(s)
