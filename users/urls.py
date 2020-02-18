from rest_framework import routers
from django.urls import path, include, re_path

from .views import (
    UserAllViewSet,
    AuthViewSet,
    UserOfRoleViewSet,
    UserOfDepartmentViewSet,
    UserOfParentViewSet,
    #ValidatePhoneSendOTP, 
    #ValidateOTP, 
)


# app_name = 'users'

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
router.register('userofdepartment', UserOfDepartmentViewSet, basename='auth')
router.register('userofrole', UserOfRoleViewSet, basename='auth')
router.register('userofparent', UserOfParentViewSet, basename='auth')
router.register('users', UserAllViewSet)

urlpatterns = router.urls
