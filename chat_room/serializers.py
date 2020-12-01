from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from chat_room.models import Room, Chat


class UserSerializer(serializers.ModelSerializer):
    """Сериализация пользователя"""
    class Meta:
        model = User
        fields = ("id", "username")


class RoomSerializers(serializers.ModelSerializer):
    """Сериализация комнат чата"""
    creator = UserSerializer()
    invited = UserSerializer(many=True)

    class Meta:
        model = Room
        fields = ("id", "creator", "invited", "date")


class ChatSerializers(serializers.ModelSerializer):
    """Сериализация чата"""
    user = UserSerializer()

    class Meta:
        model = Chat
        fields = ("user", "text", "date")


class ChatSerializer(serializers.ModelSerializer):
    """Сериализация чата"""
    user = UserSerializer()

    class Meta:
        model = Chat
        fields = ('id', 'room', "user", "text", "date")

class ChatPostSerializers(serializers.ModelSerializer):
    """Сериализация чата"""
    class Meta:
        model = Chat
        fields = ("room", "text")


class ChatPostSerializer(serializers.ModelSerializer):
    """Сериализация чата"""
    class Meta:
        model = Chat
        fields = ("room",'user', "text")