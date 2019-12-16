from django.contrib import admin
from .models import New, Genre, NewsTag


@admin.register(New)
class NewAdmin(admin.ModelAdmin):
    pass


admin.site.register(NewsTag)
admin.site.register(Genre)
