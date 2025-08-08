from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Product
from .serializers import ProductSerializer, ProductDetailSerializer
from .permissions import IsAdminOrReadOnly
from .pagination import StandardResultsSetPagination


class ProductListApiView(generics.ListAPIView):
    queryset = Product.objects.select_related('category').order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated] # Только зарегистрированным
    lookup_field = "pk"
