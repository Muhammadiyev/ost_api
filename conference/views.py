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
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from rest_framework.views import APIView
from django.conf import settings
from otp.models import PhoneOTP
import random
from django.template.loader import render_to_string

User = get_user_model()


def send_email(email, user):
    
    context = {
        'conference': Conference.objects.filter().order_by('-created_at').first()
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
    permission_classes = []
    queryset = Conference.objects.all()
    serializer_class = serializers.ConferenceSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['typeconf', 'user']

    def create(self, request, *args, **kwargs):
        userIds = request.data.getlist('usersofroleofdepartments')
        phone = User.objects.filter(
            id__in=userIds).values_list('phone', flat=True)
        phone_number = list(phone)
        # print(phone_number)

        if len(phone_number) != 0:
            for ph in phone_number:
                # print(ph)
                phone = str(ph)
                user = User.objects.filter(phone__iexact=phone)
                key = send_otp(phone)
                if key:
                    PhoneOTP.objects.create(
                        phone=phone,
                        otp=key
                    )
                else:
                    return Response({'status': False, 'detail': 'Sending otp error'})

        response = super(ConferenceViewSet, self).create(
            request, *args, **kwargs)

        email = User.objects.filter(
            id__in=userIds).values_list('email', flat=True)
        #print(request.data['user'])
        print(request.data)
        send_email(email,user)
        return Response({'status': True, 'detail': 'OTP EMAIL sent successfully'})


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
