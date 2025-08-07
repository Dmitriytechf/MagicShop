from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


from .models import Order, ShipingAdress


@shared_task
def send_order_confirmation(order_id):
    '''
    Celery задача для отправки подтверждения заказа по электронной почте.
    '''
    order = Order.objects.get(id=order_id)
    # Тема письма с номером заказа
    subject = f'Order {order.id} payment Confirmation'
    # Данные адреса доставки
    receipent_data = ShipingAdress.objects.get(user=order.user)
    # Извлекаем email из данных доставки
    receipent_email = receipent_data.email
    message = f'Ваш заказ подтвержден. Номер Вашего заказа {order.id}. Ждите, скоро с вашим заказом прилетит волшебная сова!'

    mail_to_sender = send_mail(
        subject, message=message, from_email=settings.EMAIL_HOST_USER, recipient_list=[receipent_email],
    )

    return mail_to_sender
