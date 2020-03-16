from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import UploadedFile
from . import serializers
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt import authentication
from rest_framework.views import APIView
from django.conf import settings
from rest_framework import viewsets, status


class UploadedFileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UploadedFile.objects.all()
    serializer_class = serializers.UploadedFileSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['company', 'user']