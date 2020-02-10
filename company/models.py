from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _


class Company(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(
        upload_to='company/images/', null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(null=False, default=now)

    def __str__(self):
        return "%s" % self.name


class Department(models.Model):
    department_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(null=False, default=now)
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.CASCADE)
    company = models.ForeignKey(
        Company, null=True, related_name='department_of_company', on_delete=models.CASCADE)
    status = models.BooleanField(_('status_user'), default=True)
    conference = models.BooleanField(_('conference_user'), default=True)
    
    def __str__(self):
        return "%s" % self.department_name

    @property
    def users(self):
        return self.user_of_department