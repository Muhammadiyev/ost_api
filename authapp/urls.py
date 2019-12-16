from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from .views import (
    GroupViewSet,
    PermissionViewSet,
    UserActivationView,
    UnsubscribeView
)
router = routers.DefaultRouter()

router.register('groups', GroupViewSet)
router.register('permissions', PermissionViewSet)


urlpatterns = [
    path('', include(router.urls)),
    url(r'^auth/users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$',
        UserActivationView.as_view()),
    url(r'^auth/users/unsubscribe/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$',
        UnsubscribeView.as_view()),
]
