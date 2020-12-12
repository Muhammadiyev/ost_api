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
    security_room = models.CharField(max_length=1000000, null=True, blank=True)
    waiting_room = models.BooleanField(_('waiting_room'), default=True)
    video_organizer = models.BooleanField(_('video_organizer'), default=True)
    video_participant = models.BooleanField(_('video_participant'), default=True)
    entrance_organizer = models.BooleanField(_('entrance_organizer'), default=True)
    off_participant_volume = models.BooleanField(_('off_participant_volume'), default=True)
    administrator = models.IntegerField(blank=True, default=0)
    conf_protected_sms = models.BooleanField(_('conf_protected_sms'), null=True, default=True)

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


class OneToOneConf(models.Model):
    creator = models.ForeignKey(
        'users.CustomUser', blank=True, null=True, on_delete=models.CASCADE, related_name="creator_of_user")
    invited = models.ForeignKey(
        'users.CustomUser', blank=True,null=True, on_delete=models.CASCADE, related_name="invited_of_user")
    rating = models.IntegerField(blank=True, default=0)
    status_call = models.BooleanField(_('status_call'), default=True)
    status = models.BooleanField(_('status'), default=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return f"{self.creator} - {self.invited} - {self.rating}"


    
class SettingsConf(models.Model):
    creator = models.ForeignKey(
        'users.CustomUser', blank=True, null=True, on_delete=models.CASCADE, related_name="settings_creator_of_user")
    conf = models.ForeignKey(
        Conference, blank=True,null=True, on_delete=models.CASCADE, related_name="conf_of_conference")
    audio_muted = models.ManyToManyField(
        CustomUser, blank=True, related_name="audio_of_users")
    video_muted = models.ManyToManyField(
        CustomUser, blank=True, related_name="video_of_users")
    record_users = models.ManyToManyField(
        CustomUser, blank=True, related_name="record_of_users")
    demostration_users = models.ManyToManyField(
        CustomUser, blank=True, related_name="demostration_of_users")
    blocked_users = models.ManyToManyField(
        CustomUser, blank=True, related_name="blocked_of_users")
    in_record = models.ManyToManyField(
        CustomUser, blank=True, related_name="in_record_of_users")
    in_demonstration = models.ManyToManyField(
        CustomUser, blank=True, related_name="in_demonstration_of_users")
    administrator = models.IntegerField(blank=True,null=True, default=0)

    def __str__(self):
        return f"{self.creator} "