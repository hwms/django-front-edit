from django.utils import six

str = six.text_type
chr = six.unichr

if six.PY2:  # pragma: no cover
    def viewitems(obj, **kwargs):  # pragma: no cover
        """py2 viewitems"""
        return obj.viewitems(**kwargs)

    def unpack(packed):
        if len(packed) == 2:
            return packed[0], packed[1]
        return packed[0], None
else:  # pragma: no cover
    def viewitems(obj, **kwargs):  # pragma: no cover
        """py3 viewitems"""
        return obj.items(**kwargs)

    def unpack(packed):
        val1, *val2 = packed
        if len(val2) == 1:
            return val1, val2[0]
        return val1, None
