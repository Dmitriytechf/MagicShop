from django.test import TestCase
from django.urls import reverse


class OtherAppViewTest(TestCase):
    def test_contact_view(self):
        """
        Тестирование страницы контактов
        """
        url = (reverse('otherapp:contact'))
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'otherapp/contact.html')
    
    def test_about_us_view(self):
        """
        Тестирование страницы информации о компании
        """
        url = (reverse('otherapp:other'))
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'otherapp/about_us.html')
