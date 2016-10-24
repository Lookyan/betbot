PYTHON=python
PYTHONPATH=./
SOURCE_DIR=./
TESTS_DIR=./tests

all: help

help:
	@echo "test         - run tests"

test:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m unittest discover $(TESTS_DIR) -v
