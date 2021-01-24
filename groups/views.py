from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Message, Room
from . import serializers
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt import authentication
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
from rest_framework.views import APIView
from django.db.models import Q

User = get_user_model()


class MessageAPIView(generics.ListAPIView):
    permission_classes = []
    queryset = Message.objects.all()
    serializer_class = serializers.MessageSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['room','conference']


class Rooms(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all()
    serializer_class = serializers.RoomSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['conference', 'invited', 'creator']

class RoomsGetViews(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all()
    serializer_class = serializers.RoomGetSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['conference', 'invited', 'creator']