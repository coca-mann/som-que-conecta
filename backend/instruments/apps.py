from django.apps import AppConfig


class InstrumentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.instruments'

    def ready(self):
        import backend.instruments.signals