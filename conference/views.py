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
from rest_framework_simplejwt import authentication
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from rest_framework.views import APIView
from django.conf import settings
from otp.models import PhoneOTP
from rest_framework import permissions, static, generics
from permissions.permissions import UserHasPermission, IsAdminOrConferenceOwner
import random
from django.template.loader import render_to_string

import requests

User = get_user_model()


def send_email(email):

    context = {
        'conference': Conference.objects.filter().last()
    }
    email_html_message = render_to_string('email/send_email.html', context)
    email_plaintext_message = render_to_string('email/send_email.txt', context)
    email = EmailMultiAlternatives(
        'your colleagues created a video confession',
        email_html_message,
        settings.DEFAULT_FROM_EMAIL,
        email,
        # reply_to=(email,),
    )
    email.attach_alternative(email_html_message, "text/html")
    email.send()


class ConferenceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conference.objects.all()
    serializer_class = serializers.ConferenceSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['typeconf', 'user']

    def create(self, request, *args, **kwargs):
        response = super(ConferenceViewSet, self).create(
            request, *args, **kwargs)
        userIds = request.data['usersofroleofdepartments']
        phone = User.objects.filter(
            id__in=userIds).values_list('phone', flat=True)
        phone_number = list(phone)

        if len(phone_number) != 0:
            for ph in phone_number:
                phone = str(ph)
                user = User.objects.filter(phone__iexact=phone)
                key = send_otp(phone)
                if key:
                    PhoneOTP.objects.create(phone=phone, otp=key)
                
                    payload = {'msisdn': phone, 'text': key, 'id': 0,'login' : "orientsoft", 'password': 'Or!enT$ofT', 'ref-id': 0,'version':1.0}
                    r = requests.get('http://91.204.239.42:8081/re-smsbroker', params=payload)
                    
        email = User.objects.filter(
            id__in=userIds).values_list('email', flat=True)
        send_email(email)
        return response
        
def send_otp(phone):
    if phone:
        key = random.randint(9999, 99999)
        return key
    else:
        return False


class ConferenceGetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conference.objects.all()
    serializer_class = serializers.ConferenceGetSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['typeconf', 'user']


class ConfUserIDViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conference.objects.all()
    serializer_class = serializers.ConfUserIDSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['typeconf', 'user']

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticated]
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAdminOrConferenceOwner]

        return [permission() for permission in permission_classes]


class ConferenceUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ConferenceUser.objects.all()
    serializer_class = serializers.ConferenceUserSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['see_user', 'conference']


class TypeConfViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TypeConf.objects.all()
    serializer_class = serializers.TypeConfSerializer
    authentication_classes = [authentication.JWTAuthentication, ]


class ConferencePhoneViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conference.objects.all()
    serializer_class = serializers.ConferenceSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['usersofroleofdepartments']

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.last()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    return Response({
                        'status': True,
                        'detail': 'OTP MATCHED.'
                    })
                else:
                    return Response({
                        'status': False,
                        'detail': 'OTP INCOORECT'
                    })
            else:
                return Response({
                    'status': False,
                    'detail': 'First proceed via sending otp request'
                })
        else:
            return Response({
                'status': False,
                'detail': 'Please provide both phone and otp for validated'
            })
