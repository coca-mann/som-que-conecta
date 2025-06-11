from django.apps import AppConfig


class LessonsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.lessons'

    def ready(self):
        # Importa os signals para que eles sejam registrados quando a app carregar.
        import backend.lessons.signals