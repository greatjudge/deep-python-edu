SHELL := /bin/bash

main:
	python3 -m venv venv; \
	source venv/bin/activate; \
	python -m pip install ujson faker; \
	python setup.py install; \

test: main
	python -m unittest tests.py