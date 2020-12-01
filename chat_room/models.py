from django.db import models
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
User = get_user_model()

class ThreadManager(models.Manager):

    # method to grab the thread for the 2 users
    def get_or_new(self, user, other_username): # get_or_create
        username = user.username
        if username == other_username:
            return None, None
        # looks based off of either username
        qlookup1 = Q(user__username=username)
        qlookup2 = Q(user__username=other_username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            return None, False


class Room(models.Model):
    """Модель комнаты чата"""
    creator = models.ForeignKey(User, null=True, blank=True, verbose_name="Создатель", on_delete=models.CASCADE)
    invited = models.ManyToManyField(User, blank=True, verbose_name="Участники", related_name="invited_user")
    date = models.DateTimeField("Дата создания", auto_now_add=True)

    # def __str__(self):
    #     return f"{self.creator} - {self.invited} - {self.rating}"
        
    class Meta:
        verbose_name = "Комната чата"
        verbose_name_plural = "Комнаты чатов"


class Chat(models.Model):
    """Модель чата"""
    room = models.ForeignKey(Room,null=True,blank=True, verbose_name="Комната чата", on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True,blank=True, verbose_name="Пользователь", on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=500)
    date = models.DateTimeField("Дата отправки", auto_now_add=True)

    objects      = ThreadManager()

    class Meta:
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чатов"



