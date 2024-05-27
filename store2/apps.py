from django.apps import AppConfig


class Store2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store2'

    def ready(self):
        import store2.signals
