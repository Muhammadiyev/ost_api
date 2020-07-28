from rest_framework import routers
from django.urls import path, include, re_path

from .views import (
    TypeConfViewSet,
    ConferenceViewSet, 
    ConferenceFViewSet,
    ConferenceUserViewSet, 
    ConferenceGetViewSet,
    ConferencePhoneViewSet,
    ConfUserIDViewSet,
    ConfUsersIDViewSet,
    ConferenceUserIDViewSet
)

app_name = 'conference'

router = routers.DefaultRouter(trailing_slash=False)

router.register('typeconference', TypeConfViewSet)
router.register('conferenceoff', ConferenceViewSet)
router.register('conferenceon', ConferenceFViewSet)
router.register('conference', ConferenceGetViewSet)
router.register('conferenceuser', ConferenceUserViewSet)
router.register('phone', ConferencePhoneViewSet)
router.register('confuserid', ConfUserIDViewSet)
router.register('confusers', ConferenceUserIDViewSet)

router.register('confusersid', ConfUsersIDViewSet)


urlpatterns = router.urls

