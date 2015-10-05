from django.utils import six

str = six.text_type
chr = six.unichr

if six.PY2:  # pragma: no cover
    def viewitems(obj, **kwargs):  # pragma: no cover
        """py2 viewitems"""
        return obj.viewitems(**kwargs)
else:  # pragma: no cover
    def viewitems(obj, **kwargs):  # pragma: no cover
        """py3 viewitems"""
        return obj.items(**kwargs)
