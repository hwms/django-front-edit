from __future__ import unicode_literals
from django import forms

def make_form(edit_class, fields):
    return type(b'EditFormFor{}'.format(edit_class.__name__),
        (forms.ModelForm,),
        dict(
            form_fields=forms.CharField(initial=','.join(fields),
                widget=forms.HiddenInput()),
            Meta=type(b'Meta', (object,),
                dict(model=edit_class, fields=fields)
            )
        )
    )
