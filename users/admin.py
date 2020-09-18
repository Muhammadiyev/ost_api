from django.contrib import admin
from .models import CustomUser, CheckPasswordUser

admin.site.register(CustomUser)
admin.site.register(CheckPasswordUser)
