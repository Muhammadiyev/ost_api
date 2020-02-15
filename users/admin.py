from django.contrib import admin
from .models import CustomUser, CreateUserMany, PhoneOTP

admin.site.register(CustomUser)
admin.site.register(PhoneOTP)

admin.site.register(CreateUserMany)
