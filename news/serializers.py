from rest_framework import serializers
#from .models import New, Genre, NewsTag
from users.models import CustomUser
from comment.serializers import CommentSerializer


# class NewsTagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NewsTag
#         fields = '__all__'


# class GenreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Genre
#         fields = ('name', 'alias')


# class NewsSerializer(serializers.ModelSerializer):

#     author = serializers.ReadOnlyField(source='author.email')
#     genre = GenreSerializer(read_only=True)

#     class Meta:
#         model = New
#         fields = '__all__'
