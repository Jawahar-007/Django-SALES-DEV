from django.apps import AppConfig


class SalesappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'salesapp'

    #Register cache signals
    def ready(self):
        from . import signals