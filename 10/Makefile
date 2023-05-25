SHELL := /bin/bash

main:
	python3 -m venv venv
	source venv/bin/activate
	python setup.py install

test: main
	python -m unittest test.py