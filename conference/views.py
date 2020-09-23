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
from django.db.models import Count, Sum, Max, Min,Avg, F,BooleanField, Case, When, Q, IntegerField, FloatField


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
                    payload = {'msisdn': phone}
                    r = requests.get('http://91.204.239.42/stop_all?action=delete&',params=payload)
                    payload = {'msisdn': phone, 'text': "vconf.pager.uz sizni konferentsiyaga taklif qiladi: kirish uchun KOD: %s" % key, 'priority':"1", 'id': 0,'delivery-notification-requested' : 'true','login' : settings.SMS_LOGIN, 'password': settings.SMS_PASSWORD, 'ref-id': 0,'version':1.0}
                    r = requests.get(settings.SMS_URL, params=payload)
                    
        email = User.objects.filter(
            id__in=userIds).values_list('email', flat=True)
        send_email(email)

        return response
    
    def update(self, request, *args, **kwargs):
        response = super(ConferenceViewSet, self).update(
            request, *args, **kwargs)
        userIds = request.data['usersofroleofdepartments']
        users = request.data['user']
        username = User.objects.filter(
            id__in=users).values_list('first_name', flat=True)
        user_conf = list(username)

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
                    payload = {'msisdn': phone}
                    r = requests.get('http://91.204.239.42/stop_all?action=delete&',params=payload)
                    payload = {'msisdn': phone, 'text':"(eslatma) vconf.pager.uz konferensiya kirish uchun KOD: %s" % key, 'priority':"1", 'id': 0,'delivery-notification-requested' : 'true','login' : settings.SMS_LOGIN, 'password': settings.SMS_PASSWORD, 'ref-id': 0,'version':1.0}
                    r = requests.get(settings.SMS_URL, params=payload)

        return response


class ConferenceUpdatedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conference.objects.all()
    serializer_class = serializers.ConferenceSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['typeconf', 'user']

    def update(self, request, *args, **kwargs):
        response = super(ConferenceUpdatedViewSet, self).create(
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
                    payload = {'msisdn': phone}
                    r = requests.get('http://91.204.239.42/stop_all?action=delete&',params=payload)
                    payload = {'msisdn': phone, 'text': key, 'priority':"1", 'id': 0,'delivery-notification-requested' : 'true','login' : settings.SMS_LOGIN, 'password': settings.SMS_PASSWORD, 'ref-id': 0,'version':1.0}
                    r = requests.get(settings.SMS_URL, params=payload)
                    
        email = User.objects.filter(
            id__in=userIds).values_list('email', flat=True)
        send_email(email)
        return response


class ConferenceFViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conference.objects.all()
    serializer_class = serializers.ConferenceOnSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['typeconf', 'user']

    def create(self, request, *args, **kwargs):
        response = super(ConferenceFViewSet, self).create(
            request, *args, **kwargs)
        userIds = request.data['usersofroleofdepartments']
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


class ConferenceListViewSet(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Conference.objects.all().order_by('-created_at')
    serializer_class = serializers.ConferenceGetSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['usersofroleofdepartments', 'user__company','user']
    

class ConfUsersIDViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conference.objects.all().order_by('-id')
    serializer_class = serializers.ConfUsersIDSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['usersofroleofdepartments', 'typeconf','user']


class ConferenceUserIDViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conference.objects.all()
    serializer_class = serializers.ConfeUsersIDSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['usersofroleofdepartments', 'typeconf','user']
    

class ConfUserIDViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conference.objects.all()
    serializer_class = serializers.ConfUserIDSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['usersofroleofdepartments', 'typeconf','user']

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


class StatisticConferenceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Conference.objects.all()
    serializer_class = serializers.StatisticConferenceSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['typeconf','user']

    def get_queryset(self):
        queryset = Conference.objects.all()
        queryset = queryset.values('typeconf','user').annotate(
            static_conf=Count('user')) 
         
        return queryset


class StatisticConferenceUsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.StatisticConferenceUsersSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['id','conference_of_users__typeconf']
    
    def get_queryset(self):
        queryset = User.objects.all()
        queryset = queryset.values('conference_of_users__typeconf','id').annotate(
            static=Count('conference_of_users',distinct=True )) 
         
        return queryset
