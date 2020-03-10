from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

__all__ = [
    'EmailSerializer',
    'PasswordTokenSerializer',
    'TokenSerializer',
]


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordTokenSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)                              
    token = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
