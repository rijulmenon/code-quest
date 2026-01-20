from django.apps import AppConfig

class CodestarConfig(AppConfig):
    name = 'codestar'
    default_auto_field = 'django.db.models.BigAutoField'

from django.apps import AppConfig

class CodestarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'codestar'

    def ready(self):
        import codestar.signals