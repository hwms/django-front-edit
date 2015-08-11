

try:#PY2
    import __builtin__

    chr = unichr
    range = xrange
    str = unicode

except ImportError:#PY3
    import builtins

    chr = builtins.chr
    range = builtins.range
    str = builtins.str

def viewitems(obj, **kwargs):# pragma: no cover
    """py2/3 viewitems"""
    func = getattr(obj, 'viewitems', None)
    if not func:
        func = obj.items
    return func(**kwargs)
