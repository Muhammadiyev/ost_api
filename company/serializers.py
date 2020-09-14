from django.contrib.auth import get_user_model, password_validation
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager
from .models import Company, Department
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


class UserOfDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id','first_name', 'last_name', 'midname', 'username', 'email', 'phone', 'department',
                  'parent', 'company']

class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name', 'image','user_of_company']


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['id', 'department_name_uz','department_name_ru', 'user','parent']


class DepartmentOfUserSerializer(serializers.ModelSerializer):
    children = DRecursiveSerializer(read_only=True, many=True)

    class Meta:
        model = Department
        fields = ['id', 'user_of_department','user',
                  'parent', 'department_name_uz', 'department_name_ru','children']


class DepartmentOfUsersSerializer(serializers.ModelSerializer):
    children = DRecursiveSerializer(read_only=True, many=True)
    user_of_department = UserOfDepartmentSerializer(read_only=True, many=True)

    class Meta:
        model = Department
        fields = ['id', 'user_of_department','user',
                  'parent', 'department_name_uz', 'department_name_ru','children']


class StatisticDepartmentSerializer(serializers.ModelSerializer):
    static_department = serializers.IntegerField(read_only=True)

    class Meta:
        model = Department
        fields = ['id','static_department',
                 'department_name_uz', 'department_name_ru']

