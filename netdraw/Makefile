#
# Makefile for netdraw program.
#
# By Nick Pascucci

# We use hyphen prefixes to ignore failures.
test:
	- python client_test.py
	- python display_test.py
	- python server_test.py

lint:
	pylint --errors-only *.py
