from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from chat_room.models import Room, Chat
from chat_room.serializers import (RoomSerializers, ChatSerializers, ChatPostSerializers,  UserSerializer)

from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
#from rest_framework_simplejwt import authentication
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse, HttpResponse
User = get_user_model()
from django.shortcuts import render, get_object_or_404



def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]


def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Room, creator=user)


def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)


class Rooms(APIView):
    """Комнаты чата"""
    permission_classes = []

    def get(self, request):
        rooms = Room.objects.filter(Q(creator=request.user) | Q(invited=request.user))
        serializer = RoomSerializers(rooms, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        Room.objects.create(creator=request.user)
        return Response(status=201)

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Chat.objects.all().order_by('-id')
    serializer_class = ChatPostSerializers
    #authentication_classes = [authentication.JWTAuthentication, ]
    # filter_backends = (filters.DjangoFilterBackend,
    #                    SearchFilter, OrderingFilter)
    # filter_fields = ['sender', 'receiver']

class Dialog(APIView):
    """Диалог чата, сообщение"""
    permission_classes = []
    # permission_classes = [permissions.AllowAny, ]

    def get(self, request):
        room = request.GET.get("room")
        chat = Chat.objects.filter(room=room)
        serializer = ChatSerializers(chat, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        # room = request.data.get("room")
        dialog = ChatPostSerializers(data=request.data)
        if dialog.is_valid():
            dialog.save(user=request.user)
            return Response(status=201)
        else:
            return Response(status=400)


class AddUsersRoom(APIView):
    """Добавление юзеров в комнату чата"""
    permission_classes = []
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        room = request.data.get("room")
        user = request.data.get("user")
        try:
            room = Room.objects.get(id=room)
            room.invited.add(user)
            room.save()
            return Response(status=201)
        except:
            return Response(status=400)
