from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Room(models.Model):
    """Модель комнаты чата"""
    creator = models.ForeignKey(User, verbose_name="Создатель",related_name='room_of_user', on_delete=models.CASCADE)
    invited = models.ManyToManyField(User, verbose_name="Участники", related_name="room_of_invited_user")
    date = models.DateTimeField("Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Комната чата"
        verbose_name_plural = "Комнаты чатов"

class Message(models.Model):
    contact = models.ForeignKey(
        Room, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username

class Chat(models.Model):
    """Модель чата"""
    room = models.ForeignKey(Room,blank=True,null=True, verbose_name="Комната чата", on_delete=models.CASCADE)
    user = models.ForeignKey(User,blank=True,null=True, verbose_name="Пользователь", on_delete=models.CASCADE)
    message = models.TextField("Сообщение", max_length=500)
    date = models.DateTimeField("Дата отправки", auto_now_add=True)

    class Meta:
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чатов"



