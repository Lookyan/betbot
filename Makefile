PYTHON=python
PYTHONPATH=./
SOURCE_DIR=./
TESTS_DIR=./tests/bin

all: help

help:
	@echo "test         - run tests"

test:
	$(PYTHON) -m unittest discover $(TESTS_DIR) -v
