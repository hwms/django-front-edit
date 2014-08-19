from __future__ import unicode_literals
from .conf import register_setting

__version_raw__ = ['1', '0']
__version__ = VERSION = '.'.join(__version_raw__)
def get_version():# pragma: no cover
    '''get the version number'''
    return VERSION

DEFER = '__front_edit_defer'

SETTINGS = dict(
    LOGOUT_URL_NAME='admin:logout',
    CUSTOM_FIELDS=[],
    INLINE_EDITING_ENABLED=True,
    LOADER_TEMPLATE='front_edit/loader.html',
    TOOLBAR_TEMPLATE='front_edit/includes/toolbar.html',
    EDITABLE_TEMPLATE='front_edit/includes/editable.html'
)

register_setting(SETTINGS, 'FRONT_EDIT')
