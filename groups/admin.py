from django.contrib import admin
from .models import (
    Group, 
    GroupChat, 
    GroupUser, 
    Message,
    Room
)

admin.site.register(Room)
admin.site.register(Group)
admin.site.register(GroupChat)
admin.site.register(GroupUser)
admin.site.register(Message)
