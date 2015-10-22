from django.template import Library
register = Library()
# must go below for circular import
from .tags import Edit, EditLoader
