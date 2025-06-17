from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.articles'

    def ready(self):
        import backend.articles.signals
