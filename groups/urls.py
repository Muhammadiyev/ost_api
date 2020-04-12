from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from .views import (
    MessageViewSet,
    GroupChatViewSet,
    GroupUserViewSet,
    GroupViewSet,
    Rooms,
    RoomsGetViews
)


router = routers.DefaultRouter(trailing_slash=False)
router.register('message', MessageViewSet)
router.register('groupchat', GroupChatViewSet)
router.register('groupuser', GroupUserViewSet)
router.register('group', GroupViewSet)
router.register('rooms', Rooms)
router.register('roomsget', RoomsGetViews)

urlpatterns = router.urls

# urlpatterns = [
#     path('room/', Rooms.as_view()),
#     # path('dialog/', Dialog.as_view()),
#     # path('users/', AddUsersRoom.as_view()),
# ]