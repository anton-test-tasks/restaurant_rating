from django.shortcuts import render
from django.http import HttpResponseForbidden
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from . import serializers
from . import models
from django.contrib.auth.models import User


class Pagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class RestaurantView(viewsets.ModelViewSet):
    model = models.Restaurant
    queryset = models.Restaurant.objects
    serializer_class = serializers.RestaurantSerializer
    pagination_class = Pagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter]
    ordering_fields = ['overall_rating']
    ordering = ['overall_rating']
    search_fields = ['name', 'food_type', 'address']
    filterset_fields = ['name', 'food_type', 'address']
    http_method_names = ['get', 'post', 'patch', 'delete']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)


class RatingView(viewsets.ModelViewSet):
    model = models.Rating
    queryset = models.Rating.objects
    serializer_class = serializers.RatingSerializer
    pagination_class = Pagination
    filter_backends = [filters.OrderingFilter]
    ordering = ['rating']
    ordering_fields = ['rating']
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        user_ratings = models.Rating.objects.filter(user=self.request.user)
        return user_ratings

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.user.id == self.request.user.id:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return HttpResponseForbidden()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserRegisterView(viewsets.ModelViewSet):
    model = User
    queryset = User.objects
    serializer_class = serializers.UserSerializer
    http_method_names = ['post']
    permission_classes = [AllowAny]


class UserGetUpdateView(viewsets.ModelViewSet):
    model = User
    queryset = User.objects
    serializer_class = serializers.UserSerializer
    http_method_names = ['get', 'patch']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = User.objects.filter(id=self.request.user.id)
        return user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.id == self.request.user.id:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return HttpResponseForbidden()
