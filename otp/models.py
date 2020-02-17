from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now
from company.models import Role, Department
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

class PhoneOTP(AbstractBaseUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$', message="Phone number   must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone = models.CharField(
        validators=[phone_regex], max_length=17, blank=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    validated = models.BooleanField(
        default=False, help_text='If it is true, that means user have validate otp correctly in second API')

    def __str__(self):
        return str(self.phone) + 'is sent ' + str(self.otp)