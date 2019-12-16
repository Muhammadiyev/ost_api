from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('base-auth/', include('rest_framework.urls')),
    path('', include('authapp.urls')),
    path('api/v1/', include('comment.urls')),
    path('api/v1/', include('news.urls')),
    path('auth/', include('djoser.urls')),
    path('auth_token/', include('djoser.urls.authtoken')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
