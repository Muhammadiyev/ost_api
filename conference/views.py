from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import TypeConf, ConferenceUser, Conference
from . import serializers
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import authentication
from users.models import PhoneOTP
import random

User = get_user_model()


class ConferenceViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = Conference.objects.all()
    serializer_class = serializers.ConferenceSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['typeconf', 'user']

    # def create(self, request, *args, **kwargs):
    #     userIds = request.data.getlist('usersofroleofdepartments')
    #     phone_number = User.objects.filter(id__in=userIds).values_list('phone', flat=True)
    #     phone_numbers = list(phone_numbers)

    def create(self, request, *args, **kwargs):
        userIds = request.data.getlist('usersofroleofdepartments')
        phone = User.objects.filter(
            id__in=userIds).values_list('phone', flat=True)
        phone_number = list(phone)
        print(phone_number)
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({'status': False, 'detail': 'phone number already exist'})
            else:
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact=phone)
                    if old.exists():
                        old = old.first()
                        count = old.count
                        if count > 10:
                            return Response({
                                'status': False,
                                'detail': 'Sending otp error. Limit exceeded. Please contact customer support.'
                            })

                        old.count = count + 1
                        old.save()
                        print('count increase', count)
                        return Response({
                            'status': True,
                            'detail': 'OTP sent successfully'
                        })
                    else:

                        PhoneOTP.objects.create(
                            phone=phone,
                            otp=key
                        )
                        return Response({
                            'status': True,
                            'detail': 'OTP sent successfully'
                        })
                else:
                    return Response({'status': False, 'detail': 'Sending otp error'})
        else:
            return Response({'status': False, 'detail': 'Phone number is not given in post request'})


def send_otp(phone):
    if phone:
        key = random.randint(9999, 99999)
        return key
    else:
        return False


class ConferenceUserViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = ConferenceUser.objects.all()
    serializer_class = serializers.ConferenceUserSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['see_user', 'conference']


class TypeConfViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = TypeConf.objects.all()
    serializer_class = serializers.TypeConfSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
