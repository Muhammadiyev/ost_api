from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager
from .models import (
    Conference, 
    ConferenceUser, 
    TypeConf, 
    OneToOneConf,
    SettingsConf
)
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
                  'save_conf', 'start_time', 'protected', 'status','security_room','conf_protected_sms',
                  'start_status', 'user','usersofroleofdepartments','created_at']


class ConferenceOnSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Conference
        fields = ['id', 'theme', 'description', 'timezone','when','not_limited',
                  'duration', 'typeconf','save_conf', 'start_time', 'protected', 'status',
                  'start_status', 'user','usersofroleofdepartments','created_at','security_room','conf_protected_sms',
                  'waiting_room','video_organizer','video_participant','entrance_organizer','off_participant_volume']

class StatisticConferenceSerializer(serializers.ModelSerializer):

    static_conf = serializers.IntegerField(read_only=True)
    typeconf = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField(read_only=True)

    class Meta:
        model = Conference
        fields = ['id','user','typeconf', 'static_conf']


class StatisticConferenceUsersSerializer(serializers.ModelSerializer):

    static = serializers.IntegerField(read_only=True)
   
    conference_of_users__typeconf = serializers.IntegerField(read_only=True)
    #conference_of_user = serializers.IntegerField()

    class Meta:
        model = User
        fields = ['id','conference_of_users__typeconf', 'static']
        

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
        fields = ['id', 'theme', 'when', 'status', 'user']


class ConfeUsersIDSerializer(serializers.HyperlinkedModelSerializer):
    user = UserOfConfSerializer(read_only=True)
    usersofroleofdepartments = UsersAllSerializer(many=True)
    id = serializers.IntegerField()

    class Meta:
        model = Conference
        fields = ['id', 'theme', 'description', 'timezone','when','not_limited', 'duration',
                  'save_conf', 'start_time', 'protected', 'status','start_status','user','usersofroleofdepartments','created_at']

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
   
        return super(ConfeUsersIDSerializer, self).update(instance, validated_data)
        

class ConfUserIDSerializer(serializers.HyperlinkedModelSerializer):
    user = UserOfConfSerializer(read_only=True)
    usersofroleofdepartments = UsersAllSerializer(many=True)
    id = serializers.IntegerField()

    class Meta:
        model = Conference
        fields = ['id', 'administrator', 'theme', 'description', 'timezone','when','not_limited', 'duration',
                  'save_conf', 'start_time', 'protected', 'status','start_status','user',
                  'usersofroleofdepartments','created_at','room_name','security_room',
                  'waiting_room','video_organizer','video_participant','entrance_organizer','off_participant_volume']

    # def to_representation(self, data):
    #     data = super(ConfUserIDSerializer, self).to_representation(data)
    #     data['security_room'] = True if data['security_room'] != None else data['security_room'] == True
    #     return data

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

class OneToOneConfSerializer(serializers.ModelSerializer):

    class Meta:
        model = OneToOneConf
        fields = ['id', 'creator','invited','status_call','status']


class OneToOneConfListSerializer(serializers.ModelSerializer):
    creator = UsersAllSerializer(read_only=True)
    invited = UsersAllSerializer(read_only=True)

    class Meta:
        model = OneToOneConf
        fields = ['id', 'creator','invited','status_call','status']


class SettingsConfSerializer(serializers.ModelSerializer):

    class Meta:
        model = SettingsConf
        fields = ['id', 'creator','conf','audio_muted','video_muted',
        'record_users','demostration_users','blocked_users','in_record','in_demonstration','administrator']
