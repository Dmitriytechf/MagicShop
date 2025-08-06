from django.db import models
from django.contrib.auth import get_user_model

from shop.models import Product


User = get_user_model()


class ShipingAdress(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField('email address', max_length=255)

    # Adress
    street_adress = models.CharField(max_length=255)
    apartment_adress = models.CharField(max_length=255)
    country =  models.CharField(max_length=255)
    city =  models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Country: {self.country}; City: {self.city}. Customer: {self.user}'
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)
    shipping_adress = models.ForeignKey(ShipingAdress, on_delete=models.CASCADE,
                             blank=True, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order: {str(self.id)} | Total price: {self.amount}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                             blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                             blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)
    
    def __str__(self):
        return f'Order Item: {str(self.id)} | Price: {self.price}'
