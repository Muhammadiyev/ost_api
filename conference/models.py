from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser
from django.db.models import DurationField
import pytz
import random
import string
from django_rest_passwordreset.tokens import get_token_generator
from users.fields import OrderField

TOKEN_GENERATOR_CLASS = get_token_generator()


class TypeConf(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "%s" % self.name

TYPE_CONFERENCE_CHOICES = [
    (1 , "Conference"),
    (2 , 'Vebinar')
]

class Conference(models.Model):

    @staticmethod
    def generate_key():
        """ generates a pseudo random code using os.urandom and binascii.hexlify """
        return TOKEN_GENERATOR_CLASS.generate_token()

    theme = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    user = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE, blank=True, related_name="conference_of_user")
    when = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    not_limited = models.BooleanField(_('not_limited'), default=False)
    typeconf = models.IntegerField(blank=True, null=True, choices=TYPE_CONFERENCE_CHOICES, default=1)
    save_conf = models.BooleanField(_('save_conference'), default=False)
    start_time = models.CharField(max_length=100, blank=True)
    protected = models.BooleanField(_('protected_conference'), default=True)
    status = models.BooleanField(_('status'), default=True)
    start_status = models.BooleanField(_('start_status'), default=True)
    usersofroleofdepartments = models.ManyToManyField(
        CustomUser, blank=True, related_name="conference_of_users")
    room_name = models.CharField(max_length=1000000, blank=True)
    security_room = models.CharField(max_length=1000000, blank=True)
    waiting_room = models.BooleanField(_('waiting_room'), default=True)
    organizer = models.BooleanField(_('organizer'), default=True)
    participant = models.BooleanField(_('participant'), default=True)
    entrance_organizer = models.BooleanField(_('entrance_organizer'), default=True)
    entrance_participant = models.BooleanField(_('entrance_participant'), default=True)


    def __str__(self):
        return "%s" % self.theme

    def save(self, *args, **kwargs):
        if not self.room_name:
            self.room_name = self.generate_key()
        return super(Conference, self).save(*args, **kwargs)

class ConferenceUser(models.Model):
    conference = models.ForeignKey(
        Conference, on_delete=models.CASCADE, related_name="conferenceuser_of_conference")
    see_user = models.ForeignKey(
        CustomUser, blank=True, on_delete=models.CASCADE, related_name="conferenceuser_of_customuser")
    number_users = models.IntegerField(blank=True)
    status = models.BooleanField(_('status_user'), default=True)

    def __str__(self):
        return "%s" % self.number_users

    # class Meta:
    #     verbose_name = 'Фирма'
    #     verbose_name_plural = 'Фирмы'
