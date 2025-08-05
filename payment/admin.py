from django.contrib import admin

from .models import ShipingAdress, Order, OrderItem


admin.site.register(ShipingAdress)
admin.site.register(Order)
admin.site.register(OrderItem)
