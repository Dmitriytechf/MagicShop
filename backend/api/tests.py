from account.models import Profile
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from shop.models import Category, Product

from .serializers import (ProductDetailSerializer, ProductSerializer,
                          ProfileSerializer)


class APIViewTest(APITestCase):
    '''
    Тестировние API на основные запросы
    '''
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(name="Test Category")
        self.product1 = Product.objects.create(title="Bla Bla", 
                                               category=self.category, 
                                               slug="bla-bla")
        self.product2 = Product.objects.create(title="Bla Bla2", 
                                               category=self.category, 
                                               slug="bla-bla2")

    def test_get_all_products(self):
        '''Тест на получение всех продуктов'''
        url = reverse('api:products')
        response = self.client.get(url)

        # Сортируем по id для правильной пагинации
        products = Product.objects.all().order_by('id')
        #  many=True т.к. проверяем список объектов
        serializers = ProductSerializer(products, many=True)

        self.assertEqual(response.data['results'], serializers.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_api_view(self):
        '''Тест на получение конкретного продукта'''
        url = reverse('api:products-detail', kwargs={'pk': self.product1.pk})
        response = self.client.get(url)

        serializers = ProductDetailSerializer(self.product1)

        self.assertEqual(response.data, serializers.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_api_view(self):
        '''Тест на получение профиля пользователя(никнейма и аватарки)'''
        url = reverse('api:profile')
        response = self.client.get(url)

        profile = Profile.objects.all().order_by('id')
        serializers = ProfileSerializer(profile, many=True)

        self.assertEqual(response.data['results'], serializers.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
