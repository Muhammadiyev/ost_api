from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import GroupUser, GroupChat, Group, Message
from . import serializers
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt import authentication
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
User = get_user_model()


class GroupChatViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = GroupChat.objects.all()
    serializer_class = serializers.GroupChatSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['user', 'group']


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['user']


class GroupUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = GroupUser.objects.all()
    serializer_class = serializers.GroupUserSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['user', 'group']


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all().order_by('-id')
    serializer_class = serializers.MessageSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['sender', 'receiver']


@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(
            sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = serializers.MessageSerializer(
            messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = serializers.MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
