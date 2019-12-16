from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuthappConfig(AppConfig):
    name = 'authapp'
    verbose_name = _('authapp')

    def ready(self):
        import authapp.signals
