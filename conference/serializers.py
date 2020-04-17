from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager
from .models import TypeConf, Conference, ConferenceUser
from users.serializers import UserOfConferenceSerializer, CustomUserCreateSerializer, UserOfConfSerializer, UsersAllSerializer

User = get_user_model()


class TypeConfSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeConf
        fields = ('id', 'name')


class ConferenceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Conference
        fields = ['id', 'theme', 'description', 'timezone','when','not_limited', 'duration', 'typeconf',
                  'save_conf', 'start_time', 'protected', 'status','start_status', 'user','usersofroleofdepartments','created_at','room_name']

class ConferenceGetSerializer(serializers.ModelSerializer):
    user = UserOfConfSerializer(read_only=True)
    
    class Meta:
        model = Conference
        fields = ['id', 'theme', 'description', 'timezone','when','not_limited', 'duration', 'typeconf',
                  'save_conf', 'start_time', 'protected', 'status','start_status', 'user','usersofroleofdepartments','created_at']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = [
            'id',
            'order',
            'email',
            'username'
        ]

class UsersIdSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = [
            'id',
        ]

class ConfUsersIDSerializer(serializers.HyperlinkedModelSerializer):
    user = UsersIdSerializer(read_only=True)
    class Meta:
        model = Conference
        fields = ['id', 'theme', 'when', 'user']


class ConfUserIDSerializer(serializers.HyperlinkedModelSerializer):
    user = UserOfConfSerializer(read_only=True)
    usersofroleofdepartments = UsersAllSerializer(many=True)
    id = serializers.IntegerField()

    class Meta:
        model = Conference
        fields = ['id', 'theme', 'description', 'timezone','when','not_limited', 'duration',
                  'save_conf', 'start_time', 'protected', 'status','start_status','user','usersofroleofdepartments','created_at','room_name']

    def update(self, instance, validated_data):
        all_users_data = validated_data.pop('usersofroleofdepartments')
        for usersofroleofdepartments in all_users_data:
            if 'id' in usersofroleofdepartments:
                parcel_id = usersofroleofdepartments.pop('id')
                User.objects.update_or_create(id=parcel_id, defaults=usersofroleofdepartments)
            else:
                user_id = validated_data['id']
                usersofroleofdepartments = User.objects.create(user_id=user_id,**usersofroleofdepartments)
                instance.usersofroleofdepartments.add(usersofroleofdepartments)
   
        return super(ConfUserIDSerializer, self).update(instance, validated_data)


class ConferenceUserSerializer(serializers.ModelSerializer):
    conference = ConferenceSerializer()
    #see_user = UserOfConferenceSerializer()

    class Meta:
        model = ConferenceUser
        fields = ['id', 'conference', 'see_user', 'number_users',
                  'status']
