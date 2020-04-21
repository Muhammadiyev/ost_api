from django.db import models

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser
from django.db.models import DurationField
from django.contrib.auth import get_user_model, password_validation

User = get_user_model()


class Contact(models.Model):
    user = models.ForeignKey(
        User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', blank=True)
    created_at = models.DateTimeField(null=False, default=now)
    status = models.BooleanField(_('public_conference'), default=True)

    def __str__(self):
        return self.user.username


class Message(models.Model):
    contact = models.ForeignKey(
        Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    conference = models.ForeignKey('conference.Conference',null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.contact.user.username


class Chat(models.Model):
    participants = models.ManyToManyField(
        Contact, related_name='chats', blank=True)
    messages = models.ManyToManyField(Message, blank=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    file = models.FileField(upload_to='chat', blank=True)
    conference = models.ForeignKey('conference.Conference',null=True, blank=True, on_delete=models.CASCADE)
    status = models.BooleanField(_('public_conference'), default=True)

    def __str__(self):
        return "{}".format(self.pk)