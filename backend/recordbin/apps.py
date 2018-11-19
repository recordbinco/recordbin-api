from django.apps import AppConfig


class RecordBinConfig(AppConfig):
    name = "backend.recordbin"

    def ready(self):
        from .signals import create_auth_token
