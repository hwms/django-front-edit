from __future__ import unicode_literals
from django.utils.encoding import smart_str
from django import forms

def make_form(edit_class, fields):
    return type(
        smart_str('EditFormFor{}'.format(edit_class.__name__)),
        (forms.ModelForm,),
        dict(
            form_fields=forms.CharField(
                initial=','.join(fields), widget=forms.HiddenInput()),
            Meta=type(smart_str('Meta'), (object,),
                      dict(model=edit_class, fields=fields))
        )
    )
