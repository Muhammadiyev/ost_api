from django.urls import path, include, re_path

from .views import ValidateOTP


urlpatterns = [
    re_path('^validate_otp/$', ValidateOTP.as_view()),
]
