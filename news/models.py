from django.db import models
from django.conf import settings
from datetime import datetime
from authapp.models import CustomUser
from django.utils.encoding import python_2_unicode_compatible


class Genre(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Жанры'
        verbose_name_plural = 'Жанры'


class NewsTag(models.Model):
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name


class New(models.Model):
    genre = models.ForeignKey(Genre, blank=True, null=True,
                              default=None, on_delete=models.CASCADE, related_name="books")
    title = models.CharField(max_length=225)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='user_img', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='News author+')
    tag = models.ManyToManyField('NewsTag', blank=True)
    is_active = models.BooleanField(default=False)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    publish_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '"%s" by %s' % (self.title, self.author)
