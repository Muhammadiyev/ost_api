from django.db import models

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser
from django.db.models import DurationField
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()

class Room(models.Model):
    """Модель комнаты чата"""
    room_name = models.CharField(max_length=100,blank=True)
    creator = models.ForeignKey(User, verbose_name="Создатель", blank=True,null=True, on_delete=models.CASCADE, related_name="room_of_user")
    invited = models.ForeignKey(User, verbose_name="Участник", blank=True,null=True, on_delete=models.CASCADE, related_name="room_invited_user")
    timestamp = models.DateTimeField("Дата создания", auto_now_add=True)
    created_at = models.DateTimeField(null=False, default=now)
    status = models.BooleanField(_('public_conference'), default=True)
    conference = models.ForeignKey('conference.Conference',null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Комната чата"
        verbose_name_plural = "Комнаты чатов"


class Message(models.Model):
    room = models.ForeignKey(Room,blank=True,null=True,  verbose_name="Комната чата", on_delete=models.CASCADE)
    sender = models.ForeignKey(
        CustomUser,blank=True,null=True, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        CustomUser,blank=True,null=True, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    file = models.FileField(upload_to='chat', blank=True)
    conference = models.ForeignKey('conference.Conference',null=True, blank=True, on_delete=models.CASCADE)
    status = models.BooleanField(_('public_conference'), default=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
