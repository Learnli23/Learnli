from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
class ModerationConfig(AppConfig):
    name = 'moderation'
    def  ready(self):
          import users.signals  # import signals modules to register signala