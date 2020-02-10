from django.db import models

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser
from django.db.models import DurationField


class Group(models.Model):
    name = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE, related_name="group_of_user")
    status = models.BooleanField(_('public_conference'), default=True)

    def __str__(self):
        return "%s" % self.name


class GroupChat(models.Model):
    created_at = models.DateTimeField(null=False, default=now)
    user = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE, related_name="groupchat_of_user")
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="groupchat_of_group")
    status = models.BooleanField(_('public_conference'), default=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return "%s" % self.user


class GroupUser(models.Model):
    user = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE, related_name="groupuser_of_user")
    groug = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="groupuser_of_gruop")
    created_at = models.DateTimeField(null=False, default=now)

    def __str__(self):
        return "%s" % self.user


class Message(models.Model):
    sender = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)
