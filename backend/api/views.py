from account.models import Profile
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from payment.models import Order
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.models import Product

from .pagination import StandardResultsSetPagination
from .permissions import IsAdminOnly, IsAdminOrReadOnly
from .serializers import (OrderSerializer, ProductDetailSerializer,
                          ProductSerializer, ProfileSerializer)


class ProductListApiView(generics.ListAPIView):
    '''API функция списка продуктов'''
    queryset = Product.objects.select_related('category').order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination


class ProductDetailAPIView(generics.RetrieveAPIView):
    '''API функция отдельного продукта'''
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = []  # Отключает троттлинг
    lookup_field = "pk"


class ProfileAPIView(generics.ListAPIView):
    '''API функция акаунта пользователя'''
    queryset = Profile.objects.all().order_by('id')
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination


class OrderAPIView(generics.RetrieveAPIView):
    '''API функция заказа пользователя'''
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminOnly] # Разрешаем только админу читать данные
    pagination_class = StandardResultsSetPagination
