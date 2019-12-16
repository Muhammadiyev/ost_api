from django.db import models
from news.models import New
from authapp.models import CustomUser


class Comment(models.Model):
    parentComment = models.ForeignKey(
        'self', blank=True, null=True, related_name='subcomments', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True, auto_now=False)
    news = models.ForeignKey(New, blank=True, null=True,
                             related_name='news', on_delete=models.CASCADE)
    author = models.ForeignKey(
        CustomUser, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.author

    class Meta:
        verbose_name = 'Коментарии'
        verbose_name_plural = 'Коментарии'
