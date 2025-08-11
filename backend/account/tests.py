from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class AccountViewTest(TestCase):
    '''Тест основных функций акаунта'''
    def setUp(self):
        # Создаем тестового пользователя
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass12345'
        )

    def test_account_profile_anonim(self):
        '''Тестирование профиля акаунта для анонима'''
        url = (reverse('account:profile'))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_account_profile(self):
        '''Тестирование профиля акаунта'''
        self.client.login(username='testuser', password='testpass12345')
        url = reverse('account:profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile/profile.html')

    def test_account_delete(self):
        '''Тестирование удаления акаунта'''
        self.client.login(username='testuser', password='testpass12345')

        # Проверяем, что пользователь существует
        self.assertTrue(User.objects.filter(username='testuser').exists())

        url = reverse('account:delete_account')
        response = self.client.post(url)

        # Проверка редиректа
        self.assertRedirects(response, reverse('shop:products'))
        # Проверяем, что пользователь удален
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_successful_password_change(self):
        """Тест успешной смены пароля"""
        self.client.login(username='testuser', password='testpass12345')
        data = {
            'old_password': 'testpass12345',
            'new_password1': 'new_strong_password123',
            'new_password2': 'new_strong_password123'
        }
        url = reverse('account:change_password')
        response = self.client.post(url, data)
        
        # Проверяем редирект
        self.assertRedirects(response, reverse('account:profile'))

        # Проверяем, что пароль действительно изменился
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_strong_password123'))
