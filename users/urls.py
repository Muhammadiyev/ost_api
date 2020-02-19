from rest_framework import routers
from django.urls import path, include, re_path

from .views import (
    UserAllViewSet,
    AuthViewSet,
    UserOfRoleOfDepartmentViewSet,
    UserOfDepartmentViewSet,
    UserOfRoleOfViewSet,
)


router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
router.register('userofdepartment', UserOfDepartmentViewSet, basename='auth')
router.register('userofroleofdepartment',
                UserOfRoleOfDepartmentViewSet, basename='auth')
router.register('userofrole', UserOfRoleOfViewSet, basename='auth')
router.register('users', UserAllViewSet)

urlpatterns = router.urls
