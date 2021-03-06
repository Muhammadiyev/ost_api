from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views
from users.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('api/', include('otp.urls')),
    path('api/v1/', include('company.urls')),
    path('api/v1/', include('news.urls')),
    path('api/v1/', include('conference.urls', namespace='conference')),
    path('api/v1/', include('groups.urls')),
    path('api/v1/', include('uploaded_choices.urls')),
    path('base-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth_token/', include('djoser.urls.authtoken')),

    url(r'^api/password_reset/',
        include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
