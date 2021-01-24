from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager
from .models import Message, Room
from users.models import CustomUser
from users.serializers import UserOfRoleSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""
    class Meta:
        model = User
        fields = ("id", "username")


class RoomSerializer(serializers.ModelSerializer):
    """Сериализация комнат чата"""

    class Meta:
        model = Room
        fields = ("id",'room_name', "creator", "invited",'conference', "timestamp",'status')

class RoomGetSerializer(serializers.ModelSerializer):
    """Сериализация комнат чата"""
    creator = UserSerializer()
    invited = UserSerializer()

    class Meta:
        model = Room
        fields = ("id",'room_name', "creator", "invited",'conference', "timestamp",'status')

class MessageSerializer(serializers.ModelSerializer):
    """Сериализация чата"""
    # sender = UserSerializer()
    # receiver = UserSerializer()
    username = serializers.CharField(read_only=True)

    class Meta:
        model = Message
        fields = ('id','username', "user",'receiver', "message", "timestamp",'status','conference')


class MessagePostSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Message
        fields = ['id','room', 'user','receiver', 'message', 'timestamp','file','is_read','conference','status']