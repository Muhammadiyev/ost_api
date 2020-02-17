from django.contrib import admin
from .models import CustomUser, CreateUserMany

admin.site.register(CustomUser)

admin.site.register(CreateUserMany)
