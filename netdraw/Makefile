#
# Makefile for netdraw program.
#
# By Nick Pascucci

# We use hyphen prefixes to ignore failures.

OLDPYTHONPATH = $(PYTHONPATH)
MODULE_DIR = $(shell dirname $(PWD))

test:
	export PYTHONPATH=$(PYTHONPATH):$(MODULE_DIR)
	- python client_test.py
	- python display_test.py
	- python server_test.py
	export PYTHONPATH=$(OLDPYTHONPATH)

lint:
	pylint --errors-only *.py

clean:
	rm *.pyc

dist: clean
	tar -cf netdraw.tar client.py display.py server.py