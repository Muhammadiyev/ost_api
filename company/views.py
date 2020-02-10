from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Department
from . import serializers
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import authentication
User = get_user_model()


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Department.objects.all()
    serializer_class = serializers.DepartSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['company']


class DepartmentOfUserViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentOfUserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['parent', 'company']
