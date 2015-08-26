"""AppSettings Class and utils"""

import re
from django.conf import settings as master_settings
from django.utils.encoding import python_2_unicode_compatible
from functools import wraps

from .compat import str, viewitems

CAMELCASE = re.compile(r'(.)([A-Z])([^A-Z])')
ENDSETTINGS = re.compile(r'(.*?)(_SETTINGS)')

@python_2_unicode_compatible
class Default(object):#pylint: disable=too-few-public-methods
    """A default AppSetting that looks into the django.conf.settings file"""
    def __init__(self, name, fallback):
        """pass the name of the setting and a fallback value"""
        self.name = name
        self.fallback = fallback

    def get(self):
        """get the setting value"""
        return getattr(master_settings, self.name, self.fallback)

    def __str__(self):
        return str(self.get())

class AppSettings(object):#pylint: disable=too-few-public-methods
    """AppSettings can be defined in a subclass using class variables"""
    def __init__(self):
        """setup the app settings"""
        prefix = CAMELCASE.sub(r'\1_\2\3', self.__class__.__name__).upper()
        prefix = ENDSETTINGS.sub(r'\1', prefix)
        setting = dict([(attr, getattr(self, attr))
                        for attr in dir(self)
                        if not attr.startswith("_")
                        and not callable(getattr(self, attr))])
        master_name = '{}_SETTINGS'.format(prefix)
        # get overrides in dict form
        setting.update(getattr(master_settings, master_name, dict()))
        for k, val in viewitems(setting):
            # set default value based on some other setting
            if isinstance(val, Default):
                val = str(val)
            name = '{}_{}'.format(prefix, k)
            # get individual override and modify
            master_val = self.do_mod(k, getattr(master_settings, name, val))
            # update attr in this class
            setattr(self, k, master_val)

    def do_mod(self, name, val):
        """preform a modification lookup and call the function"""
        return getattr(self, 'mod_{}'.format(name.lower()), lambda s: s)(val)

    def __repr__(self):
        return '<{} {}>'.format(
            self.__class__.__name__,
            dict([(attr, getattr(self, attr))
                  for attr in dir(self)
                  if not attr.startswith("_")
                  and not callable(getattr(self, attr))]))

def override_appsettings(**settings_kwargs):
    """override an appsetting, used for unit testing"""
    from .settings import appsettings
    def wrap(func):
        """receive the func"""
        @wraps(func)
        def wrap_func(*args, **kwargs):
            """wrap the func and receive the args
                perform the override of appsettings
            """
            old = {}
            for key, val in viewitems(settings_kwargs):
                old[key] = getattr(appsettings, key)
                setattr(appsettings, key, val)
            func(*args, **kwargs)
            for key, val in viewitems(old):
                setattr(appsettings, key, val)
        return wrap_func
    return wrap
