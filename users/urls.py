from rest_framework import routers
from django.urls import path, include, re_path

from .views import (
    UserAllViewSet,
    AuthViewSet,
    UserOfRoleSerializerViewSet,
    UserOfDepartmentViewSet,
    UserOfParentSerializerViewSet,
    #ValidatePhoneSendOTP, 
    #ValidateOTP, 
)


# app_name = 'users'

router = routers.DefaultRouter(trailing_slash=False)
router.register('api/auth', AuthViewSet, basename='auth')
router.register('userofdepartment', UserOfDepartmentViewSet, basename='auth')
router.register('userofrole', UserOfRoleSerializerViewSet, basename='auth')
router.register('userofparent', UserOfParentSerializerViewSet, basename='auth')
router.register('users', UserAllViewSet)

urlpatterns = router.urls


# urlpatterns = [
#     re_path(r'^validate_phone/', ValidatePhoneSendOTP.as_view()),
#     re_path('^validate_otp/$', ValidateOTP.as_view()),
# ]