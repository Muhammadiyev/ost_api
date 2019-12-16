from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from .views import (
    NewsViewSet,
)

router = routers.DefaultRouter()

router.register('news', NewsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
