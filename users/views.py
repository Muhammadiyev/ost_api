from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import CustomUser, CreateUserMany
from . import serializers
from .utils import get_and_authenticate_user, create_user_account
from rest_framework import authentication
from rest_framework_simplejwt import authentication
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from django.http.response import HttpResponse
from rest_framework import permissions, static, generics
from django.shortcuts import get_object_or_404
from permissions.permissions import UserHasPermission
from rest_framework_simplejwt.exceptions import TokenBackendError, TokenError, InvalidToken
import random
from .authentication import AUTH_HEADER_TYPES
User = get_user_model()


class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = serializers.TokenRefreshSerializer


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'password_change': serializers.PasswordChangeSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class UserAllViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserProfileSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['parent', 'company']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [UserHasPermission]

        return [permission() for permission in permission_classes]


class UserOfDepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserOfDepartmentSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['parent', 'company']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [UserHasPermission]

        return [permission() for permission in permission_classes]


class UserOfRoleOfViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserOfRoleSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['parent', 'company']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [UserHasPermission]

        return [permission() for permission in permission_classes]


class UserOfRoleOfDepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserOfRoleOfDepartmentRoleSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['parent', 'company']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [UserHasPermission]

        return [permission() for permission in permission_classes]
