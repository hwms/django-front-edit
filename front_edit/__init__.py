'''
A front end editing app for Django.

This app allows one to edit dynamic data on the front end of a website when
logged in as a staff member. The app allows the editing of dynamic content
within any element.
'''
from __future__ import unicode_literals

import django

__version__ = '1.2.1'

if django.VERSION < (1, 7):
    from . import settings
