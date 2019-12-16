from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'news'
    verbose_name = ('news')

    def ready(self):
        import news.signals
