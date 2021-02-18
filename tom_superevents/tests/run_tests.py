#!/usr/bin/env python
# run_tests.py
#
# To run:
#   cd /path/to/tom_superevents  # top-level directory
#   python tom_superevents/tests/run_tests.py
#


from django.core.management import call_command
from boot_django import boot_django, APP_NAME  # noqa


boot_django()
print(f'Running tests for {APP_NAME}')
call_command('test', APP_NAME, verbosity=2)

# TODO: consider collecting switches and arguments
#  from the command line (like -v or a specific test module
#  or function) and passing them on to call command
