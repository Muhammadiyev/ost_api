from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from .managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now
from company.models import  Department
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.contrib.auth import models as auth_models
from django.db.models.manager import EmptyManager
from django.utils.functional import cached_property
from rest_framework_simplejwt.compat import CallableFalse, CallableTrue
from .settings import api_settings
from users.fields import OrderField

def validate_image(fieldfile_obj):
    filesize = fieldfile_obj.file.size
    megabyte_limit = 2.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'username', blank=True, max_length=50, unique=True)
    email = models.EmailField('email address',blank=True,unique=True)
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
    last_seen = models.CharField(max_length=100, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    city = models.CharField(max_length=100,blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    department = models.ForeignKey(
        Department, blank=True, null=True, related_name="user_of_department", on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    status = models.BooleanField(_('status_user'), default=True)
    conference = models.BooleanField(_('conference_user'), default=True)
    online_user = models.BooleanField(_('online_user'), default=False)
    company = models.ForeignKey(
        'company.Company', blank=True, null=True, related_name="user_of_company", on_delete=models.CASCADE)
    order = models.IntegerField(default=1,blank=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'phone'
    #REQUIRED_FIELDS = ['phone']

    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def users(self):
        return self.conference_of_users

    def get_short_name(self):
        return self.phone

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return f"{self.phone} - {self.email} - {self.username}"


class CheckPasswordUser(models.Model):
    creator_user = models.ForeignKey(
        'CustomUser', blank=True, null=True, related_name="creator_user", on_delete=models.CASCADE)
    user = models.ForeignKey(
        'CustomUser', blank=True, null=True, related_name="user", on_delete=models.CASCADE)
    check_password = models.CharField(
        'check_password', blank=True, max_length=150)
    is_active = models.BooleanField(_('active'), default=True)


class TokenUser:
    """
    A dummy user class modeled after django.contrib.auth.models.AnonymousUser.
    Used in conjunction with the `JWTTokenUserAuthentication` backend to
    implement single sign-on functionality across services which share the same
    secret key.  `JWTTokenUserAuthentication` will return an instance of this
    class instead of a `User` model instance.  Instances of this class act as
    stateless user objects which are backed by validated tokens.
    """
    # User is always active since Simple JWT will never issue a token for an
    # inactive user
    is_active = True

    _groups = EmptyManager(auth_models.Group)
    _user_permissions = EmptyManager(auth_models.Permission)

    def __init__(self, token):
        self.token = token

    def __str__(self):
        return 'TokenUser {}'.format(self.id)

    @cached_property
    def id(self):
        return self.token[api_settings.USER_ID_CLAIM]

    @cached_property
    def pk(self):
        return self.id

    @cached_property
    def username(self):
        return self.token.get('username', '')

    @cached_property
    def is_staff(self):
        return self.token.get('is_staff', False)

    @cached_property
    def is_superuser(self):
        return self.token.get('is_superuser', False)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.id)

    def save(self):
        raise NotImplementedError('Token users have no DB representation')

    def delete(self):
        raise NotImplementedError('Token users have no DB representation')

    def set_password(self, raw_password):
        raise NotImplementedError('Token users have no DB representation')

    def check_password(self, raw_password):
        raise NotImplementedError('Token users have no DB representation')

    @property
    def groups(self):
        return self._groups

    @property
    def user_permissions(self):
        return self._user_permissions

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return set()

    def has_perm(self, perm, obj=None):
        return False

    def has_perms(self, perm_list, obj=None):
        return False

    def has_module_perms(self, module):
        return False

    @property
    def is_anonymous(self):
        return CallableFalse

    @property
    def is_authenticated(self):
        return CallableTrue

    def get_username(self):
        return self.username
