import json
from http import HTTPStatus

from django.contrib.sessions.middleware import SessionMiddleware

from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from shop.models import Category, ProductProxy

from .views import cart_add, cart_delete, cart_update, cart_view


class CartTest(TestCase):
    '''Тестирование представлений корзины'''
    def setUp(self):
        '''Тестовые данные'''
        self.client = Client()
        self.factory = RequestFactory().get(reverse('cart:cart-view'))
        self.middleware = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()
    
    def test_cart_view(self):
        '''Тест функции отображения корзины'''
        request = self.factory
        response = cart_view(request)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.client.get(reverse('cart:cart-view')), 'cart/cart-view.html')
        
class CartAddandDeleteViewTestCase(TestCase):
    '''Тестирование функций удаления и добавления товаров'''
    def setUp(self):
        '''Тестовые данные'''
        self.category = Category.objects.create(name='Category 1')
        self.product = ProductProxy.objects.create(title='Example Product', price=10.0, category=self.category)
        self.factory = RequestFactory().post(reverse('cart:add-to-cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 2,
        })
        self.middleware  = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()
    
    def test_cart_add(self):
        '''Тест функции добавления товара'''
        request = self.factory
        response = cart_add(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['product'], 'Example Product')
        self.assertEqual(data['qty'], 2)
    
    def test_cart_delete(self):
        '''Тест функции удаления товара'''
        request = self.factory
        response = cart_delete(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['qty'], 0)


class CartUpdateViewTestCase(TestCase):
    '''Тестирование функции обновления'''
    def setUp(self):
        '''Тестовые данные'''
        self.category = Category.objects.create(name='Category 1')
        self.product = ProductProxy.objects.create(title='Example Product', price=10.0, category=self.category)
        self.factory = RequestFactory().post(reverse('cart:add-to-cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 2,
        })
        self.factory = RequestFactory().post(reverse('cart:update-to-cart'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_qty': 3,
        })
        self.middleware  = SessionMiddleware(self.factory)
        self.middleware.process_request(self.factory)
        self.factory.session.save()
    
    def test_cart_update(self):
        '''Тест функции изменения товара в корзине'''
        request = self.factory
        response = cart_add(request)
        response = cart_update(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['total'], '30.00')
        self.assertEqual(data['qty'], 3)
