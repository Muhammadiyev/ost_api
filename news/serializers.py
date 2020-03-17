from rest_framework import serializers
from .models import News
from users.serializers import UsersAllSerializer


class NewsSerializer(serializers.ModelSerializer):

    #user = UsersAllSerializer(read_only=True)

    class Meta:
        model = News
        fields = ['id', 'title', 'description',
                  'company', 'start_date','publish_time','is_active', 'user']
