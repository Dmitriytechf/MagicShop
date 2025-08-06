from django.db import models
from django.utils.text import slugify
import random
import string
from django.urls import reverse


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

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("shop:product-detail", args=[str(self.slug)])


class ProductManager(models.Manager):
    
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(available=True)


class ProductProxy(Product):
    objects = ProductManager()
    
    class Meta:
        proxy = True
    