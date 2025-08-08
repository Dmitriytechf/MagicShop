from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Order, ShipingAdress


@shared_task
def send_order_confirmation(order_id):
    '''
    Celery задача для отправки подтверждения заказа по электронной почте.
    '''
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Order {order.id} payment Confirmation'
        
        # Получаем самый новый адрес пользователя
        shipping_address = ShipingAdress.objects.filter(user=order.user).order_by('-id').first()
        
        if not shipping_address:
            raise ValueError("No shipping address found for this user")
            
        recipient_email = shipping_address.email
        message = f'Ваш заказ подтвержден. Номер: {order.id}. Ждите доставку! Ее принесут волшебные совы!'
        
        send_mail(
            subject, 
            message=message, 
            from_email=settings.EMAIL_HOST_USER, 
            recipient_list=[recipient_email],
        )
        
    except Exception as e:
        print(f"Error sending confirmation: {e}")
