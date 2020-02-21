from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager
from .models import Company, Role, Department
from users.models import CustomUser

User = get_user_model()

class DRecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class RRecursiveSerializer(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):


    class Meta:
        model = Department
        fields = ['id','department_name']

class DepartmentOfUserSerializer(serializers.ModelSerializer):
    subparent = DRecursiveSerializer(read_only=True, many=True)

    class Meta:
        model = Department
        fields = ['id','user','parent','department_name','subparent']


class RoleOfUserSerializer(serializers.ModelSerializer):
    subparent = RRecursiveSerializer(read_only=True, many=True)

    class Meta:
        model = Role
        fields = ['id','user','parent','name','subparent']


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['id','name']