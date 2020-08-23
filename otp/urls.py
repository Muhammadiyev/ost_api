from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf import settings

from .views import ValidateOTP, download
from conference.views import ConferenceListViewSet

urlpatterns = [
    re_path('^validate_otp/$', ValidateOTP.as_view()),
    url(r'^download/(?P<path>.*)$', download),
    path('conferencelist', ConferenceListViewSet.as_view()),
]
