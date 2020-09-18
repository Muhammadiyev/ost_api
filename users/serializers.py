import re
from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model, password_validation, authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers, exceptions
from django.contrib.auth.models import BaseUserManager
from .models import CustomUser, CheckPasswordUser
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from djoser.compat import get_user_email, get_user_email_field_name
from djoser.conf import settings
from company.models import Department
from . import tokens
from company.serializers import DepartmentSerializer, CompanySerializer
import rest_auth.serializers
from django.core.validators import validate_email
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from django.core.exceptions import ValidationError
from .tokens import RefreshToken
from users.settings import api_settings as BLACKLIST_AFTER_ROTATION
from users.settings import api_settings as ROTATE_REFRESH_TOKENS

User = get_user_model()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER


def validate_image(value):
    filesize = value.size
    if filesize > 2097152:
        raise ValidationError(
            "The maximum file size that can be uploaded is 2MB")
    else:
        return value


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
        refresh = RefreshToken.for_user(user=obj)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'midname', 'username', 'email','city', 'password', 'company',
                  'parent', 'phone', 'department', 'status', 'conference', 'auth_token']
        read_only_fields = ('id', 'is_active')

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
    department = DepartmentSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    #avatar = serializers.ImageField(validators=[validate_image])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'parent', 'company', 'department', 'status', 'conference', 'first_name', 'last_name', 'midname',
                  'phone', 'last_seen', 'city', 'avatar', 'is_active','is_staff']

class UserProfileListSerializer(serializers.ModelSerializer):
    # department = DepartmentSerializer(read_only=True)
    # company = CompanySerializer(read_only=True)
    #avatar = serializers.ImageField(validators=[validate_image])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'parent', 'company', 'department', 'status', 'conference', 'first_name', 'last_name', 'midname',
                  'phone', 'last_seen', 'city', 'avatar', 'is_active','is_staff']

class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'parent',
                  'company', 'department']


class UserOfConferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email']


class EmptySerializer(serializers.Serializer):
    pass


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    def get_auth_token(self, obj):
        refresh = RefreshToken.for_user(user=obj)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_active', 'is_staff', 'company', 'auth_token')
        read_only_fields = ('id', 'is_active', 'is_staff')


class UserLoginSerializer(JSONWebTokenSerializer):
    username_field = 'username_or_phone'

    def validate(self, attrs):

        password = attrs.get("password")
        user_obj = User.objects.filter(username=attrs.get("username_or_phone")).first(
        ) or User.objects.filter(phone=attrs.get("username_or_phone")).first()
        if user_obj is not None:
            credentials = {
                'phone': user_obj.phone,
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
            msg = _('Account with this phone/username does not exists')
            raise serializers.ValidationError(msg)


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    default_error_messages = {
        'invalid_password': 'Current password does not match'
    }

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError(
                self.default_error_messages['invalid_password'])
        return value

    def validate_new_password(self, value):
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
        fields = ['id', 'username', 'email', 'order','online_user']


class UserOfRoleOfDepartmentRoleSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    children = RecursiveSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'department',
                  'parent', 'company',  'children']


class UsersAllSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    id = serializers.IntegerField()
    
    class Meta:
        model = User
        fields = ['id','order', 'username', 'email', 'parent', 'company', 'department','online_user', 'status', 'conference', 'first_name', 'last_name', 'midname',
                  'phone', 'last_seen', 'city', 'avatar', 'is_active']


class UserOfRoleSerializer(serializers.ModelSerializer):

    children = RecursiveSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'parent', 'children', 'company', ]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'phone', 'first_login']


class StatisticUsersSerializer(serializers.ModelSerializer):
    static_users = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id','static_users','city','phone','username', 'email', 'first_name']


class StatisticUsersCitySerializer(serializers.ModelSerializer):
    static_city = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id','static_city','city']


class StatisticUsersAllSerializer(serializers.ModelSerializer):
    count_users = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['count_users']

class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])

        data = {'access': str(refresh.access_token)}

        if ROTATE_REFRESH_TOKENS:
            if BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

        return data


class CheckPasswordUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CheckPasswordUser
        fields = ['id','creator_user','user','check_password','is_active']

class CheckPasswordUserListSerializer(serializers.ModelSerializer):
    
    #creator_user = UserProfileSerializer(read_only=True)
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = CheckPasswordUser
        fields = ['id','creator_user','user','check_password','is_active']
