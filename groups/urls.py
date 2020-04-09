from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers
from .views import (
    message_list,
    MessageViewSet,
    GroupChatViewSet,
    GroupUserViewSet,
    GroupViewSet
)


router = routers.DefaultRouter(trailing_slash=False)
router.register('chat', MessageViewSet)
router.register('groupchat', GroupChatViewSet)
router.register('groupuser', GroupUserViewSet)
router.register('group', GroupViewSet)

urlpatterns = router.urls
