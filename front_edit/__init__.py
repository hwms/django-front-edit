from __future__ import unicode_literals

import django

__version__ = '1.1b1'

if django.VERSION < (1, 7):
    from . import settings
