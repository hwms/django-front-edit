from __future__ import unicode_literals
import json

from django import forms
from django.utils.encoding import smart_str
from django.utils.module_loading import import_string

from .compat import viewitems


def make_form(edit_class, fields, widgets):
    field_widgets = None
    if len(widgets) == 0:
        widgets = None
    else:
        field_widgets = {k:import_string(v) for k, v in viewitems(widgets)}
    return type(
        smart_str('EditFormFor{}'.format(edit_class.__name__)),
        (forms.ModelForm,),
        dict(
            form_fields=forms.CharField(
                initial=','.join(fields), widget=forms.HiddenInput()),
            form_widgets=forms.CharField(
                initial=json.dumps(widgets), widget=forms.HiddenInput()),
            Meta=type(smart_str('Meta'), (object,),
                      dict(model=edit_class, fields=fields,
                      widgets=field_widgets))
        )
    )
