import random
import string

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

# Сделаем отдельно константы
SLUG_PREFIX = "pickBetter"

def rand_slug():
    '''Создаем строку случайных символов и букв из трех элементов'''
    rand_chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(rand_chars) for _ in range(3))


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Категория')
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children',
        blank=True, null=True, verbose_name='Родитель'
    )
    slug = models.SlugField(max_length=255, unique=True, null=False, 
                            editable=True, verbose_name='URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        # Уникалькая комбинация в БД
        unique_together = (['slug', 'parent'])
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        '''
        Формируем строковое представление объекта.
        Возвращает строку вида "Родительская категория > ... > Текущая категория"
        '''
        full_path = [self.name] # Имя текущей категории
        k = self.parent         # Родитель текущей категории 
        
        # Поднимаемся вверх по родителям, пока не дойдём до корня (parent=None)
        while k is not None:
            full_path.append(k.name) # Добавляем имя родителя в список
            k = k.parent         # Переходим к следующему родителю
        
        # Вывод будет слева направо
        return '>'.join(full_path[::-1])
    
    def save(self, *args, **kwargs):
        '''Формируем слаг если его нету'''
        if not self.slug:
            self.slug = slugify(rand_slug() + SLUG_PREFIX + self.name)
            
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop:category-list", args=[str(self.slug)])


class Product(models.Model):
    '''
    Модель продукта.
    '''
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='products')
    title = models.CharField(max_length=255, verbose_name='Навзание')
    brand = models.CharField(max_length=255, verbose_name='Бренд')
    description = models.TextField(max_length=1055, null=True, verbose_name='Описание')
    slug = models.SlugField(max_length=255, verbose_name='URL')
    price = models.DecimalField(max_digits=7, decimal_places=2,
                                default=99.99, verbose_name='Цена')
    image = models.ImageField(upload_to='products/products/%Y/%m/%d', verbose_name='Изображение')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    discount = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['created_at']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        '''Возвращает абсолютный URL для доступа к детальной странице товара.'''
        return reverse("shop:product-detail", args=[str(self.slug)])
    
    def get_discounted_price(self):
        discounted_price = self.price - (self.price * self.discount / 100)
        return round(discounted_price, 2)


class ProductManager(models.Manager):
    '''
    Кастомный менеджер для модели Product, который по умолчанию возвращает 
    только доступные товары.
    '''

    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    '''
    Прокси-модель для Product, которая использует кастомный менеджер ProductManager.
    '''
    objects = ProductManager() # Заменяем стандартный менеджер на кастомный
    
    class Meta:
        proxy = True # Указывает, что это прокси-модель
        verbose_name = 'Доступный продукт'
        verbose_name_plural = 'Доступные продукты'
    