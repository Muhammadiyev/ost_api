from django.contrib import admin
from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'parentComment', 'author', 'date', 'description']

    class Meta:
        model = Comment


admin.site.register(Comment, CommentAdmin)
