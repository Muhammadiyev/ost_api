from django.shortcuts import render
from rest_framework import generics
from .serializers import CommentSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from .models import Comment


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter()
    serializer_class = CommentSerializer
    filter_backends = (filters.DjangoFilterBackend,
                       SearchFilter, OrderingFilter)
    filter_fields = ['news']
