from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from .models import CustomUser
from .serializers import (
    CustomUserSerializer,
    PermissionSerializer,
    GroupSerializer,
)
from rest_framework import generics
from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.auth.models import User, Group, Permission
from django.http import Http404


class UserActivationView(APIView):
    @classmethod
    def get(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/auth/users/activation/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data=post_data)
        return Response(result)


class UnsubscribeView(APIView):
    @classmethod
    def get(cls, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "/auth/users/unsubscribe/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data=post_data)
        return Response(result)


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
