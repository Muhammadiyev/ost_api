from django.contrib import admin
from .models import (
    Conference, 
    ConferenceUser, 
    TypeConf, 
    OneToOneConf,
    SettingsConf
)

admin.site.register(Conference)
admin.site.register(ConferenceUser)
admin.site.register(TypeConf)
admin.site.register(OneToOneConf)
admin.site.register(SettingsConf)
