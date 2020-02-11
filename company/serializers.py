from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager
from .models import Company, Role, Department
from users.models import CustomUser
from users.serializers import UserOfRoleSerializer

User = get_user_model()



class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):

    #company = CompanySerializer(read_only=True)

    class Meta:
        model = Department
        fields = ['id','department_name', 'company',
                  'is_active', 'created_at']

class DepartmentOfUserSerializer(serializers.ModelSerializer):

    #company = CompanySerializer(read_only=True)

    class Meta:
        model = Department
        fields = ['id','department_name','user_of_department', 'company',
                  'is_active', 'created_at']


class RoleSerializer(serializers.ModelSerializer):

    #company = CompanySerializer()

    class Meta:
        model = Role
        fields = ['id', 'name', 'company',
                  'is_active', 'created_at']


class RoleOfUserSerializer(serializers.ModelSerializer):
    #user_of_department = UserOfDepartmentSerializer()
    #company = CompanySerializer()

    class Meta:
        model = Role
        fields = ['id', 'name', 'user_of_role', 'company',
                  'is_active', 'created_at']
