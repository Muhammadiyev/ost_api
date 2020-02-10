from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager
from .models import Company, Department
from users.models import CustomUser
from users.serializers import UserOfDepartmentSerializer

User = get_user_model()


class UserCompSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'email')


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class DepartSerializer(serializers.ModelSerializer):

    #company = CompanySerializer(read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'company', 'department_name', 'parent',
                  'is_active', 'status', 'conference', 'created_at']


class DepartmentSerializer(serializers.ModelSerializer):

    company = CompanySerializer()

    class Meta:
        model = Department
        fields = ['id', 'company', 'department_name', 'parent',
                  'is_active', 'status', 'conference', 'created_at']


class DepartmentOfUserSerializer(serializers.ModelSerializer):
    #user_of_department = UserOfDepartmentSerializer()
    company = CompanySerializer()

    class Meta:
        model = Department
        fields = ['id', 'user_of_department', 'company', 'department_name', 'parent',
                  'is_active', 'status', 'conference', 'created_at']