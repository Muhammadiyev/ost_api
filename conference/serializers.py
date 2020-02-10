from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager
from .models import TypeConf, Conference, ConferenceUser
# from users.models import CustomUser
from users.serializers import UserOfConferenceSerializer

User = get_user_model()


class TypeConfSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeConf
        fields = ('id', 'name')


class ConferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conference
        fields = ['id', 'theme', 'discussion', 'when', 'duration', 'typeconf',
                  'save_conf', 'start_time', 'end_time', 'protected', 'status', 'user']


class ConferenceUserSerializer(serializers.ModelSerializer):
    conference = ConferenceSerializer()
    see_user = UserOfConferenceSerializer()

    class Meta:
        model = ConferenceUser
        fields = ['id', 'conference', 'see_user', 'number_users',
                  'status']
