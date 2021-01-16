from django.contrib import admin
from .models import CustomUser, CheckPasswordUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'is_active',)
    list_filter = ('username', 'email', 'is_active',)
    fieldsets = (
        (None, {'fields': ['password', 'first_name', 'last_name', 'midname', 'username', 'email', 'phone',
                           'city', 'avatar', 'department', 'parent', 'company']}),
        ('Permissions', {'fields': ('is_active', 'is_superuser',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_active')}
         ),
    )

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(CheckPasswordUser)
