from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from users.models import CustomUser
from django.db.models import DurationField
import pytz


class TypeConf(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "%s" % self.name


class Conference(models.Model):
    theme = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(null=False, default=now)
    user = models.ForeignKey(
        'users.CustomUser', on_delete=models.CASCADE, blank=True, related_name="conference_of_user")
    when = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=100, blank=True)
    duration = DurationField(blank=True, null=True)
    not_limited = models.BooleanField(_('not_limited'), default=False)
    typeconf = models.ForeignKey(
        TypeConf, blank=True, on_delete=models.CASCADE, related_name="conference_of_type")
    save_conf = models.BooleanField(_('save_conference'), default=False)
    start_time = models.CharField(max_length=100, blank=True)
    protected = models.BooleanField(_('protected_conference'), default=True)
    status = models.BooleanField(_('public_conference'), default=True)
    usersofroleofdepartments = models.ManyToManyField(
        CustomUser, blank=True, related_name="conference_of_users")

    def __str__(self):
        return "%s" % self.theme


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
