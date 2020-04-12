from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager
from .models import Group, GroupChat, GroupUser, Message, Room
from users.models import CustomUser
from users.serializers import UserOfRoleSerializer

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name', 'user', 'status')


class GroupChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupChat
        fields = ['id', 'user', 'group', 'message', 'status', 'created_at']


class GroupUserSerializer(serializers.ModelSerializer):

    #company = CompanySerializer(read_only=True)

    class Meta:
        model = GroupUser
        fields = ['id', 'user', 'groug', 'created_at']


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""
    class Meta:
        model = User
        fields = ("id", "username")


class RoomSerializer(serializers.ModelSerializer):
    """Сериализация комнат чата"""

    class Meta:
        model = Room
        fields = ("id", "creator", "invited",'conference', "timestamp",'status')

class RoomGetSerializer(serializers.ModelSerializer):
    """Сериализация комнат чата"""
    creator = UserSerializer()
    invited = UserSerializer()

    class Meta:
        model = Room
        fields = ("id", "creator", "invited",'conference', "timestamp",'status')

class MessageSerializer(serializers.ModelSerializer):
    """Сериализация чата"""
    sender = UserSerializer()
    receiver = UserSerializer()

    class Meta:
        model = Message
        fields = ('id', "sender",'receiver', "message", "timestamp",'status','conference')


class MessagePostSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Message
        fields = ['id','room', 'sender','receiver', 'message', 'timestamp','file','is_read','conference','status']