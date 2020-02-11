from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('api/v1/', include('company.urls')),
    path('api/v1/', include('conference.urls')),
    path('api/v1/', include('groups.urls')),
    path('api/v1/', include('uploaded_choices.urls')),

    path('base-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth_token/', include('djoser.urls.authtoken')),

    url(r'^api/password_reset/',
        include('django_rest_passwordreset.urls', namespace='password_reset')),
]
if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)