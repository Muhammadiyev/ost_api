import re
from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model, password_validation, authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers, exceptions
from django.contrib.auth.models import BaseUserManager
from .models import CustomUser, CreateUserMany
from company.models import Role
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from djoser.compat import get_user_email, get_user_email_field_name
from djoser.conf import settings
from company.models import Department
from . import tokens
from company.serializers import RoleSerializer, DepartmentSerializer, RoleOfUserSerializer, CompanySerializer
import rest_auth.serializers
from django.core.validators import validate_email
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import JSONWebTokenSerializer

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    default_error_messages = {
        "cannot_create_user": settings.CONSTANTS.messages.CANNOT_CREATE_USER_ERROR
    }
    auth_token = serializers.SerializerMethodField()

    def get_auth_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    class Meta:
        model = User
        fields = ['username', settings.LOGIN_FIELD, 'password', 'company',
                  'parent', 'phone', 'role', 'department', 'status', 'conference', 'auth_token']
        read_only_fields = ('id', 'is_active', 'is_staff')

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [User._meta.pk.name, settings.LOGIN_FIELD, 'first_name', 'last_name', 'groups',
                  'user_permissions']
        read_only_fields = (settings.LOGIN_FIELD,)

    def update(self, instance, validated_data):
        email_field = get_user_email_field_name(User)
        if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.save(update_fields=["is_active"])
        return super().update(instance, validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    role = RoleOfUserSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'parent', 'company', 'department', 'role', 'status', 'conference', 'first_name', 'last_name', 'midname',
                  'phone', 'last_seen', 'city', 'avatar', 'is_active']


class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'parent',
                  'company', 'department', 'role']


class UserOfConferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'role']


class EmptySerializer(serializers.Serializer):
    pass


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    def get_auth_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_active', 'is_staff', 'company', 'auth_token')
        read_only_fields = ('id', 'is_active', 'is_staff')


def validateEmail(email):
    if len(email) > 6:
        if re.match('\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email) != None:
            return 1
    return 0


class UserLoginSerializer(JSONWebTokenSerializer):
    username_field = 'username_or_email'

    def validate(self, attrs):

        password = attrs.get("password")
        user_obj = User.objects.filter(email=attrs.get("username_or_email")).first(
        ) or User.objects.filter(username=attrs.get("username_or_email")).first()
        if user_obj is not None:
            credentials = {
                'username': user_obj.username,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    if not user.is_active:
                        msg = _('User account is disabled.')
                        raise serializers.ValidationError(msg)

                    payload = jwt_payload_handler(user)

                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user
                    }
                else:
                    msg = _('Unable to log in with provided credentials.')
                    raise serializers.ValidationError(msg)

            else:
                msg = _('Must include "{username_field}" and "password".')
                msg = msg.format(username_field=self.username_field)
                raise serializers.ValidationError(msg)

        else:
            msg = _('Account with this email/username does not exists')
            raise serializers.ValidationError(msg)


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    default_error_messages = {
        'invalid_password': 'Current password does not match'
    }

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError(
                self.default_error_messages['invalid_password'])
        return value

    def validate_new_password(self, value):
        # https://docs.djangoproject.com/en/2.0/topics/auth/passwords/#django.contrib.auth.password_validation.validate_password
        password_validation.validate_password(value)
        return value


class UserOfDepartmentSerializer(serializers.ModelSerializer):

    department = DepartmentSerializer(read_only=True)
    children = RecursiveSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'department',
                  'parent', 'children', 'company']


class UserOfConfSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserOfRoleOfDepartmentRoleSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    children = RecursiveSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'department',
                  'parent', 'company', 'role',  'children']


class UserOfRoleSerializer(serializers.ModelSerializer):

    role = RoleSerializer(read_only=True)
    children = RecursiveSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role',
                  'parent', 'children', 'company', ]


class CreateUsermanySerializer(serializers.ModelSerializer):

    class Meta:
        model = CreateUserMany
        fields = ['id', 'many_user']


class CreateUserManySerializer(serializers.ModelSerializer):
    many_user = CustomUserCreateSerializer(many=True)

    class Meta:
        model = CreateUserMany
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'phone', 'first_login']
