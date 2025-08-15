from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from shop.models import Product

User = get_user_model()


class ShipingAdress(models.Model):
    '''
    Модель адреса доставки пользователя. Обозначены все основные поля формы доставки.
    '''
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
    
    def get_absolute_url(self):
        return f"/payment/shiping"
    
    @classmethod
    def create_default_shiping_address(cls, user):
        '''Заполняет форму доставки значениями по умолчанию'''
        shipping_adress= cls.objects.create(
            user=user,
            full_name="Noname",
            email=user.email,
            street_adress="Не указано",
            apartment_adress="Не указано",
            country="Не указано",
            city="Не указано"
        )
        return shipping_adress

    class Meta:
        verbose_name = 'Адрес достваки'
        verbose_name_plural = 'Адреса доставок'
    

class Order(models.Model):
    '''Заказ пользователя.'''
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)
    shipping_adress = models.ForeignKey(ShipingAdress, on_delete=models.CASCADE,
                             blank=True, null=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False) # Подтверждение оплаты
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    def __str__(self):
        return f'Order: {str(self.id)} | Total price: {self.amount}'
    
    def get_absolute_url(self):
        return reverse("payment:order_detail", kwargs={"pk": self.pk})

    def get_total_cost_before_discount(self):
        '''Вычисляем общую сумму заказа'''
        return sum(item.get_cost() for item in self.items.all())

    @property
    def get_discount(self):
        '''Вычисляем сумму скидки в денежном выражении'''
        if (total_cost := self.get_total_cost_before_discount()) and self.discount:
            return total_cost * (self.discount / Decimal(100))
        return Decimal(0)

    def get_total_cost(self):
        '''Вычисляем итоговую стоимость'''
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"])
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(amount__gte=0),
                name='amount__gte_0'
            )
        ]


class OrderItem(models.Model):
    '''Конкретные товары в связанном заказе.'''
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                             blank=True, null=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                             blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)
    
    def __str__(self):
        return f'Order Item: {str(self.id)} | Price: {self.price}'
    
    def get_cost(self):
        return self.price * self.quantity
    
    @property
    def total_cost(self):
        return self.price * self.quantity

    @classmethod
    def get_total_quantity_for_product(cls, product):
        return cls.objects.filter(product=product).aggregate(total_quantity=models.Sum('quantity'))['total_quantity'] or 0

    @staticmethod
    def get_average_price():
        return OrderItem.objects.aggregate(average_price=models.Avg('price'))['average_price']
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-id']
        constraints = [
            models.CheckConstraint(check=models.Q(
                quantity__gt=0), name='quantity_gte_0'),
        ]
