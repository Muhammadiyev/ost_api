from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from .views import (
    Rooms,
    RoomsGetViews
)


router = routers.DefaultRouter(trailing_slash=False)
router.register('rooms', Rooms)
router.register('roomsget', RoomsGetViews)

urlpatterns = router.urls