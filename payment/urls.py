from django.urls import path, include

from .views import *
from .webhooks import stripe_webhook

app_name = 'payment'

urlpatterns = [
    # Основные действия по оформлению заказа
    path('shiping/', shiping, name='shiping'),
    path('checkout/', checkout, name='checkout'),
    path('complete-order', complete_order, name='complete-order'),
    # Результаты оформления заказа
    path('payment-success/', payment_success, name='payment-success'),
    path('payment-fail/', payment_fail, name='payment-fail'),
    # Webhook для stripe
    path('webhook-stripe/', stripe_webhook, name='webhook-stripe'),
]
