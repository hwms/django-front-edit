from .conf import AppSettings

class FrontEditSettings(AppSettings):#pylint: disable=too-few-public-methods
    """ Default settings for this app"""
    CUSTOM_FIELDS = []
    DEFER_KEY = '__front_edit_defer'
    EDITABLE_TEMPLATE = 'front_edit/includes/editable.html'
    HTML_PARSER = 'html5lib'
    INLINE_EDITING_ENABLED = True
    JQUERY_BACKUP = 'front_edit/js/jquery.min.js'
    JQUERY_BUILTIN = True
    JQUERY_CDN = '//ajax.googleapis.com/ajax/libs/jquery/'
    JQUERY_VERSION = '1.11.2'
    LOADER_TEMPLATE = 'front_edit/loader.html'
    LOGOUT_URL_NAME = 'admin:logout'
    TOOLBAR_TEMPLATE = 'front_edit/includes/toolbar.html'
    USE_HINTS = False
    VIGENERE_KEY = None

appsettings = FrontEditSettings()#pylint: disable=invalid-name
