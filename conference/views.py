from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import TypeConf, ConferenceUser, Conference
from . import serializers
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import authentication
User = get_user_model()


class ConferenceViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Conference.objects.all()
    serializer_class = serializers.ConferenceSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['typeconf', 'user']


class ConferenceUserViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = ConferenceUser.objects.all()
    serializer_class = serializers.ConferenceUserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['see_user', 'conference']


class TypeConfViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = TypeConf.objects.all()
    serializer_class = serializers.TypeConfSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
