from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now
from company.models import Role, Department
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


class CustomUser(AbstractBaseUser, PermissionsMixin):
    login = models.CharField(max_length=50, blank=True)
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('First Name', max_length=255, blank=True,
                                  null=False)
    last_name = models.CharField('Last Name', max_length=255, blank=True,
                                 null=False)
    midname = models.CharField('Mid Name', max_length=255, blank=True,
                               null=False)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,14}$', message="Phone number   must be entered in the format: '+999999999'. Up to 14 digits allowed.")
    phone = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, unique=True)
    last_seen = models.DateTimeField(null=False, default=now)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    city = models.CharField(max_length=100)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    avatar = models.ImageField(upload_to='avatars/',validators=[validate_image],help_text='Maximum file size allowed is 2Mb', null=True, blank=True)
    created_at = models.DateTimeField(null=False, default=now)
    role = models.ForeignKey(
        Role, blank=True, null=True, related_name="user_of_role", on_delete=models.CASCADE)
    department = models.ForeignKey(
        Department, blank=True, null=True, related_name="user_of_department", on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', blank=True, null=True,related_name='children', on_delete=models.CASCADE)
    status = models.BooleanField(_('status_user'), default=True)
    conference = models.BooleanField(_('conference_user'), default=True)
    company = models.ForeignKey(
        'company.Company', blank=True, null=True, related_name="user_of_company", on_delete=models.CASCADE)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = []

    @property
    def users(self):
        return self.role_of_user

    def get_short_name(self):
        return self.phone

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"


class CreateUserMany(models.Model):
    many_user = models.ManyToManyField(CustomUser)
    created_at = models.DateTimeField(null=False, default=now)
    is_active = models.BooleanField(_('active'), default=True)
