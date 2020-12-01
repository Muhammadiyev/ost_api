# coding=utf-8
from django.urls import path
from chat_room.views import *

urlpatterns = [
    path('room/', Rooms.as_view()),
    path('dialog/', Dialog.as_view()),
    path('users/', AddUsersRoom.as_view()),
    path('message/', ChatListAPIView.as_view()),
    path('message/<int:pk>/', ChatListIDAPIView.as_view()),
]
