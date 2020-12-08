from django.shortcuts import render
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import PhoneOTP, otp_expiry_time
from rest_framework_simplejwt import authentication
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from django.http.response import HttpResponse
from rest_framework import permissions, static, generics
from django.shortcuts import get_object_or_404
import random
from datetime import timedelta
from users.serializers import UserLoginSerializer
from django.utils import timezone
from conference.models import Conference

User = get_user_model()

import os
from django.conf import settings
from django.http import HttpResponse, Http404

def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404

def send_otp(phone):
    if phone:
        key = random.randint(9999, 99999)
        return key
    else:
        return False


class ValidateOTP(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication, ]

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact=phone)
            if old.exists():
                validation_time = otp_expiry_time()
                old = old.last()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    count = old.count
                    if count > 5:
                        return Response({
                            'status': False,
                            'detail': 'Sending otp error. Limit exceeded. Please contact customer support.'
                        })

                    old.count = count + 1
                    old.save()
                    if old is None:
                        return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)
                    expiry_date = old.created_at + \
                        timedelta(hours=validation_time)
                    if timezone.now() > expiry_date:
                        old.delete()
                        return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)
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


class ConfValidateKey(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.JWTAuthentication, ]

    def post(self, request, *args, **kwargs):
        id = request.data.get('id', False)
        otp_sent = request.data.get('security_room', False)

        if id and otp_sent:
            old = Conference.objects.filter(id__iexact=id)
            if old.exists():
                validation_time = otp_expiry_time()
                old = old.last()
                security_room = old.security_room
                if str(otp_sent) == str(security_room):
                    old.validated = True
                    if old is None:
                        return Response({'status': 'notfound'}, status=status.HTTP_404_NOT_FOUND)
                    expiry_date = old.created_at + \
                        timedelta(hours=validation_time)
                    if timezone.now() > expiry_date:
                        old.delete()
                        return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)
                    return Response({
                        'status': True,
                        'detail': 'SECURITY ROOM MATCHED.'
                    })
                else:
                    return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)