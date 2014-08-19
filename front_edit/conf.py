try:
    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured
except ImportError:
    settings = None # this is for setup.py when registering in pypi
from future.utils import iteritems

def register_setting(setting, prefix, modifiers=None):
    if settings is None:
        return
    # override default
    master_name = '{}_SETTINGS'.format(prefix)
    try:
        setting.update(getattr(settings, master_name, dict()))
    except ImproperlyConfigured:
        return
    if modifiers is not None:
        for key in setting:
            if key in modifiers:
                setting[key] = modifiers[key](setting[key])
    # set defaults
    setattr(settings, master_name, setting)
    # make individuals
    for k, val in iteritems(setting):
        name = '{}_{}'.format(prefix, k)
        setattr(settings, name, getattr(settings, name, val))