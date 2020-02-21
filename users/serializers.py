from django.contrib.auth import get_user_model, password_validation, authenticate
from rest_framework.authtoken.models import Token
from rest_framework import serializers
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
from company.serializers import RoleSerializer, DepartmentSerializer, RoleOfUserSerializer

User = get_user_model()


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
        fields = ['login', settings.LOGIN_FIELD, 'password', 'company',
                  'parent', 'phone', 'role', 'department', 'status', 'conference', 'auth_token']
        read_only_fields = ('id', 'is_active', 'is_staff')

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

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

    class Meta:
        model = User
        fields = ['id', 'login', 'email', 'parent', 'company', 'department', 'role', 'first_name', 'last_name', 'midname',
                  'phone', 'last_seen', 'city', 'avatar', 'is_active']


class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'login', 'email', 'parent',
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
        fields = ('id', 'email', 'first_name',
                  'last_name', 'is_active', 'is_staff', 'company', 'auth_token')
        read_only_fields = ('id', 'is_active', 'is_staff')


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


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
    subparent = RecursiveSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'login', 'email', 'department',
                  'parent', 'subparent', 'company']


class UserOfRoleOfDepartmentRoleSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    subparent = RecursiveSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'login', 'email', 'department',
                  'parent', 'company', 'role',  'subparent']


class UserOfRoleSerializer(serializers.ModelSerializer):

    role = RoleSerializer(read_only=True)
    subparent = RecursiveSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'login', 'email', 'role',
                  'parent', 'subparent', 'company', ]


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


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, data):
        print(data)
        phone = data.get("phone")
        password = data.get("password")

        if phone and password:
            if User.objects.filter(phone=phone).exists():
                print(phone, password)
                user = authenticate(request=self.context.get(
                    'request'), phone=phone, password=password)
                print(user)
            else:
                msg = {
                    'detail': 'Phone number not found',
                    'status': False
                }
                raise serializers.ValidationError(msg)
            if not user:
                msg = {
                    'detail': 'Phone number and password are not matching, Try again',
                    'status': False,
                }
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = {
                'detail': 'Phone number and password not found in request',
                'status': False
            }
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data


# class DepartSerializer(serializers.ModelSerializer):

#     department = DepartmentSerializer(read_only=True)

#     class Meta:
#         model = User
#         fields = ['id', 'department',]

    # def create(self, validated_data):
    #     department_data = validated_data.pop('department')
    #     d = Department.objects.create(**department_data)
    #     user = User.objects.create(department=d, **validated_data)
    #     user.save()
    #     return user
