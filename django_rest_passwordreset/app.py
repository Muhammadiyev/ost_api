from django.apps import AppConfig 


class DjangoRestPasswordreset(AppConfig):
    name = 'django_rest_passwordreset'
    verbose_name = 'Django Rest Passwordreset'

    def ready(self):
        import django_rest_passwordreset.signals  # noqa