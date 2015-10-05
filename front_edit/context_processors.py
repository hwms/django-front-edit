from .settings import appsettings


def defer_edit(request):
    return {appsettings.DEFER_KEY: []}
