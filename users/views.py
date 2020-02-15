from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import CustomUser, CreateUserMany, PhoneOTP
from . import serializers
from .utils import get_and_authenticate_user, create_user_account
from rest_framework import authentication
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from django.http.response import HttpResponse
from rest_framework import permissions, static, generics
from django.shortcuts import get_object_or_404
import random

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = serializers.EmptySerializer
    #authentication_classes = [authentication.TokenAuthentication, ]
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'password_change': serializers.PasswordChangeSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.set_password(
            serializer.validated_data['confirm_password'])
        request.user.save()
        return Response(status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = serializers.UserProfileSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['parent', 'company']


class UserOfDepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = serializers.UserOfDepartmentSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['parent', 'company']


class UserOfRoleSerializerViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = serializers.UserOfRoleSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['parent', 'company']


class UserOfParentSerializerViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = serializers.UserOfParentSerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['parent', 'company']


# class CreateUserManyViewSet(viewsets.ModelViewSet):
#     permission_classes = []
#     queryset = CreateUserMany.objects.all()
#     serializer_class = serializers.CreateUsermanySerializer
#     authentication_classes = [authentication.TokenAuthentication, ]

    # def get_serializer_class(self):
    #     serializer_class = serializers.CreateUsermanySerializer
    #     if self.action in ['create', 'update', 'partial_update']:
    #         serializer_class = serializers.CreateUserManySerializer
    #     return serializer_class


class ValidatePhoneSendOTP(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')
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


class ValidateOTP(APIView):

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    return Response({
                        'status': True,
                        'detail': 'OTP MATCHED. Please proceed for registration'
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
