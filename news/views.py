from django.shortcuts import render
from .serializers import NewsSerializer
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import News
from django.utils import timezone
from rest_framework_simplejwt import authentication
from django.http import Http404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter

class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = []
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    authentication_classes = [authentication.JWTAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['user', 'company']


    # def get_queryset(self):
    #     queryset = News.objects.filter(is_active=True)
    #     if self.action == 'list':
    #         queryset = News.objects.filter(
    #             is_active=True, publish_time__lte=timezone.now())
    #     return queryset

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)

    # @action(["post", 'get'], detail=True)
    # def subscribe(self, request, *args, **kwargs):
    #     news = self.get_object()
    #     if request.user not in news.subscribers.all():
    #         news.subscribers.add(request.user)
    #     else:
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     news.save()
    #     return Response(status=status.HTTP_202_ACCEPTED)

    # @action(["post", 'get'], detail=True)
    # def unsubscribe(self, request, *args, **kwargs):
    #     news = self.get_object()
    #     if request.user in news.subscribers.all():
    #         news.subscribers.remove(request.user)
    #     else:
    #         return Response(status=status.HTTP_204_NO_CONTENT)
    #     news.save()
    #     return Response(status=status.HTTP_202_ACCEPTED)
