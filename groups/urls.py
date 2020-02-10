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

router = routers.DefaultRouter()

router.register('messages', MessageViewSet)
router.register('groupchat', GroupChatViewSet)
router.register('groupuser', GroupUserViewSet)
router.register('group', GroupViewSet)


urlpatterns = [
    path('messageapi/', message_list),
    path('', include(router.urls)),
]