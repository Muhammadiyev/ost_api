from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Role, Department
from . import serializers
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import authentication
from permissions.permissions import UserHasPermission
User = get_user_model()


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = serializers.RoleSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['user']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [UserHasPermission]

        return [permission() for permission in permission_classes]


class RoleOfUserViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = serializers.RoleOfUserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['user']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [UserHasPermission]

        return [permission() for permission in permission_classes]


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['user']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [UserHasPermission]

        return [permission() for permission in permission_classes]


class DepartmentOfUserViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentOfUserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['user']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [UserHasPermission]

        return [permission() for permission in permission_classes]
