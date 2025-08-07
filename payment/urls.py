from django.urls import path, include

from .views import *
from .webhooks import stripe_webhook

app_name = 'payment'

urlpatterns = [
    path('shiping/', shiping, name='shiping'),
    path('checkout/', checkout, name='checkout'),
    path('complete-order', complete_order, name='complete-order'),
    path('payment-success/', payment_success, name='payment-success'),
    path('payment-fail/', payment_fail, name='payment-fail'),
    path('webhook-stripe/', stripe_webhook, name='webhook-stripe'),
]
