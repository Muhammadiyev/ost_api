from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager
from .models import TypeConf, Conference, ConferenceUser
from users.serializers import UserOfConfSerializer
from users.serializers import UserOfConferenceSerializer, CustomUserCreateSerializer

User = get_user_model()


class TypeConfSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeConf
        fields = ('id', 'name')


class ConferenceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Conference
        fields = ['id', 'theme', 'description', 'timezone','when','not_limited', 'duration', 'typeconf',
                  'save_conf', 'start_time', 'protected', 'status', 'user','usersofroleofdepartments','created_at','room_name']

class ConferenceGetSerializer(serializers.ModelSerializer):
    user = UserOfConfSerializer(read_only=True)
    
    class Meta:
        model = Conference
        fields = ['id', 'theme', 'description', 'timezone','when','not_limited', 'duration', 'typeconf',
                  'save_conf', 'start_time', 'protected', 'status', 'user','usersofroleofdepartments','created_at']

class ConfUserIDSerializer(serializers.ModelSerializer):
    user = UserOfConfSerializer(read_only=True)
    
    class Meta:
        model = Conference
        fields = ['id', 'theme', 'description', 'timezone','when','not_limited', 'duration', 'typeconf',
                  'save_conf', 'start_time', 'protected', 'status', 'user','usersofroleofdepartments','created_at','room_name']

class ConferenceUserSerializer(serializers.ModelSerializer):
    conference = ConferenceSerializer()
    #see_user = UserOfConferenceSerializer()

    class Meta:
        model = ConferenceUser
        fields = ['id', 'conference', 'see_user', 'number_users',
                  'status']
