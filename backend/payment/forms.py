from django import forms

from .models import Order, OrderItem, ShipingAdress


class ShipingAdressForm(forms.ModelForm):
    
    class Meta:
        model = ShipingAdress
        fields = ('full_name', 'email', 'street_adress', 'apartment_adress', 'country', 
                  'city', 'zip_code')
        exclude = ('user', )
        labels = {
            'full_name': 'Контактные данные',
            'email': 'Электронная почта',
            'street_adress': 'Адрес улицы',
            'apartment_adress': 'Адрес квартиры или дома',
            'country': 'Страна',
            'city': 'Город',
            'zip_code': 'Почтовый индекс',
        }
