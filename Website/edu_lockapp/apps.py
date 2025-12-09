from django.apps import AppConfig


class EduLockappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'edu_lockapp'

class EduLockappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'edu_lockapp'

    def ready(self):
        import edu_lockapp.signals