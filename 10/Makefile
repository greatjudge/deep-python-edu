SHELL := /bin/bash

main:
	python3 -m venv venv; \
	source venv/bin/activate; \
	python -m pip install --upgrade pip ujson faker; \
	python setup.py install; \

test: main
	venv/bin/python -m unittest tests.py;\

clean:
	rm -r build cjson.egg-info dist jsons
