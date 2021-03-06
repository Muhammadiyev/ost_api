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

    @property
    def users(self):
        return self.user_of_company


class Department(models.Model):
    department_name_uz = models.CharField(max_length=100, blank=True, null=True)
    department_name_ru = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(null=False, default=now)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    user = models.ForeignKey(
        'users.CustomUser', blank=True, null=True, related_name='department_of_user', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.department_name_uz} - {self.department_name_ru}"

    @property
    def users(self):
        return self.user_of_department
