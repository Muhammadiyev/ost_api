from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Role, Department, Company
from . import serializers
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt import authentication
from permissions.permissions import UserHasPermission
User = get_user_model()


class CompanyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Company.objects.all()
    serializer_class = serializers.CompanySerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['user_of_company']


class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = serializers.RoleSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['user_of_role']


class RoleOfUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = serializers.RoleOfUserSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['user_of_role']


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['user_of_department']


class DepartmentOfUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentOfUserSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['user_of_department']
