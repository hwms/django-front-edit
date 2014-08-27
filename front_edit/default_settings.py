from django.conf import settings

defaults = {
    'FRONT_EDIT_LOGOUT_URL_NAME': 'admin:logout',
    'FRONT_EDIT_CUSTOM_FIELDS': [],
    'FRONT_EDIT_INLINE_EDITING_ENABLED': True,
    'FRONT_EDIT_LOADER_TEMPLATE': 'front_edit/loader.html',
    'FRONT_EDIT_TOOLBAR_TEMPLATE': 'front_edit/includes/toolbar.html',
    'FRONT_EDIT_EDITABLE_TEMPLATE': 'front_edit/includes/editable.html',
}

def get_setting(name):
    result = getattr(settings, name, None)

    if result == None:
        return defaults[name]
    else:
        return result
