#!/usr/bin/env python
# django_shell.py
#
# To run:
#   cd /path/to/tom_superevents  # top-level directory
#   python tom_superevents/tests/django_shell.py
#

from django.core.management import call_command
from boot_django import boot_django  # noqa

boot_django()
call_command('shell_plus')
