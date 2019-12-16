from rest_framework import serializers
from .models import Comment
from authapp.models import CustomUser


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = ('id', 'parentComment', 'author', 'news',
                  'description', 'subcomments', 'date')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['author']

    def create(self, validated_data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        comment = Comment.objects.create(author=user, **validated_data)
        return comment
