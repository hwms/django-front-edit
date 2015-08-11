from django.apps import AppConfig

class FrontEditBackendConfig(AppConfig):
    name = 'front_edit'
    verbose_name = "Front Edit"

    def ready(self):
        from . import settings
