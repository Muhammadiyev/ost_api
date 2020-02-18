from django.contrib.auth import get_user_model, password_validation, authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager
from .models import PhoneOTP
from company.models import Role
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from djoser.compat import get_user_email, get_user_email_field_name
from djoser.conf import settings

User = get_user_model()

# class PhoneOTPerializer(serializers.ModelSerializer):

#     class Meta:
#         model = PhoneOTP
#         fields = ['id', 'phone', 'otp','validated','user']

