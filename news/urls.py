from django.conf.urls import include, url
from rest_framework import routers
from .views import NewsViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('news', NewsViewSet, basename='auth')

urlpatterns = router.urls
