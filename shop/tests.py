from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Category, ProductProxy, Product


class ProductViewTest(TestCase):
    def setUp(self):
        """
        Подготовка тестовых данных перед каждым тестом.
        """
        # Создаем тестовую категорию
        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category"
        )
        
        # Создаем тестовые продукты
        self.product_1 = ProductProxy.objects.create(
            title="Test Product1",
            slug="test-product1",
            category=self.category,
            price=100.00
        )
        
        self.product_2 = ProductProxy.objects.create(
            title="Test Product2",
            slug="test-product2",
            category=self.category,
            price=200.00
        )
    
    
    def test_get_products(self):
        """
        Тестирование списка продуктов
        """
        response = self.client.get(reverse('shop:products'))
        
        # Проверка кода ответа и тимплейта
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/products.html')
        # Проверка контекста
        self.assertEqual(response.context['products'].count(), 2)
        
        self.assertContains(response, self.product_1.title)
        self.assertContains(response, self.product_2.title)
    
    def test_get_detail_view(self):
        """
        Тестирование страницы отдельного продукта
        """
        url = reverse('shop:product-detail', kwargs={'slug': self.product_1.slug})
        response = self.client.get(url)
        
        # Проверка кода ответа и тимплейта
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_detail.html')
        # Проверка контекста
        self.assertEqual(response.context['product'], self.product_1)
        
        self.assertContains(response, self.product_1.title)

    def test_category_view(self):
        """
        Тестирование отображения продуктов по категории.
        """
        url = reverse('shop:category-list', kwargs={'slug': self.category.slug})
        response = self.client.get(url)
        
        # Проверка кода ответа
        self.assertEqual(response.status_code, 200)
        
        # Проверка шаблона
        self.assertTemplateUsed(response, 'shop/category_list.html')
        
        self.assertEqual(response.context['category'], self.category)
        