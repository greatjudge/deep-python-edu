#! /usr/bin/env python3

from setuptools import setup, Extension


def main():
    setup(
        name="cjson",
        varsion="1.0.0",
        author="Artem Galkin",
        ext_modules=[
            Extension('cjson', ['cjson.c'])
        ]
    )


if __name__ == '__main__':
    main()
