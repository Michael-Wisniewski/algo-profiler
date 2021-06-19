#!/bin/bash
SHELL := bash

include ./make/print.lib.mk

.PHONY: help
help:
	$(call print_h1,"AVAILABLE","OPTIONS")
	$(call print_space)
	$(call print_options,"test","Runs all tests")
	$(call print_options,"cov","Runs test coverage report.")
	$(call print_options,"lint","Runs black and isort.")

.PHONY: test
test:
	$(call print_h1,"STARTING","TESTS")
	@python -B -m unittest discover -v -s tests -t ${PWD} -p 'test_snakeviz.py'

.PHONY: cov
cov:
	$(call print_h1,"STARTING","TESTS", "REPORT")
	@coverage run -m unittest discover -s tests -t ${PWD}
	@coverage html
	@coverage report

.PHONY: lint
lint:
	$(call print_h1,"LAUNCHING","ISORT")
	@isort ./src
	$(call print_h1,"LAUNCHING","BLACK")
	@black ./src
	$(call print_h1,"LAUNCHING","FLAKE8")
	@flake8 --max-line-length 90 ./src/

# dodac tox
# dodac  python setup.py bdist_wheel
