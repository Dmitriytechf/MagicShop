import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Order, OrderItem, ShipingAdress


@admin.register(ShipingAdress)
class ShipingAdressAdmin(admin.ModelAdmin):
    '''Админ панель адреса доставки'''
    list_display = ('full_name_bold','user', 'email', 'country', 'city', 'zip_code')
    empty_value_display = "-empty-"
    list_display_links = ('full_name_bold',)
    list_filter = ('user', 'country', 'city')

    @admin.display(description="Full Name", empty_value="Noname")
    def full_name_bold(self, obj):
        '''Показываем имя жирным шрифтом'''
        return format_html("<b style='font-weight: bold;'>{}</b>", obj.full_name)


class OrderItemInline(admin.TabularInline):
    '''Отображение отдельных продуктов в админ панели'''
    model = OrderItem
    extra = 0 # Количество пустых форм

    def has_add_permission(self, request, obj=None):
        return False # Запрет на добавление новых OrderItem

    def has_delete_permission(self, request, obj = ...):
        return False # Запрет на удаление новых OrderItem

    def get_readonly_fields(self, request, obj=None):
        '''Как будет показываться отдельный продукт'''
        if obj:
            return ['price', 'product', "quantity", "user"]
        return super().get_readonly_fields(request, obj)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    '''Админ панель заказа'''
    list_display = ['id', 'user', 'shipping_adress', 'amount',
                    'created', 'updated', 'paid', 'order_pdf'
    ]
    list_filter = ['paid', 'updated','created',]
    inlines = [OrderItemInline] # Отображение товаров в админке заказа
    list_per_page = 15 # Пагинация
    list_display_links = ['id', 'user']

    def order_pdf(self, obj):
        url = reverse('payment:admin_order_pdf', args=[obj.id]) # Генерируем URL
        return mark_safe(f'<a href="{url}">PDF</a>') # Возвращаем HTML-ссылку

    order_pdf.short_description = 'Converting' # Заголовок столбца


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    '''Админ панель конкретного товара'''
    list_display = ['id', 'order', 'product', 'price', 'quantity']
    list_per_page = 15 # Пагинация
