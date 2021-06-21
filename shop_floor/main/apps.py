from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
    verbose_name = 'Проекты'

    def ready(self):
        from main.utils import SendNotificationThread
        thread = SendNotificationThread()
        # thread.start()
