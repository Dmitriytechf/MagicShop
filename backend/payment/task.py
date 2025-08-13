import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import Order, ShipingAdress

logger = logging.getLogger('bigcorp')

@shared_task
def send_order_confirmation(order_id):
    '''
    Celery задача для отправки подтверждения заказа по электронной почте.
    '''
    try:
        # Получаем заказ по id
        order = Order.objects.get(id=order_id)
        subject = f'Order {order.id} payment Confirmation'

        # Получаем самый новый адрес доставки пользователя
        shipping_address = ShipingAdress.objects.filter(user=order.user).order_by('-id').first()

        if not shipping_address:
            raise ValueError("No shipping address found for this user")

        # Берем email из адреса доставки и на него отправляем письмо
        recipient_email = shipping_address.email
        message = f'Ваш заказ подтвержден. Номер: {order.id}. Ждите доставку! Ее принесут волшебные совы!'

        send_mail(
            subject, # тема письма
            message=message,
            from_email=settings.EMAIL_HOST_USER, # отправитель
            recipient_list=[recipient_email], # сколько получат
        )

        logger.info(f"Письмо для заказа {order.id} успешно отправлено")

    except Order.DoesNotExist:
        error_msg = f"Заказ не был найден"
        logger.exception(error_msg)

    except Exception as e:
        error_msg = f"Ошибка при отправке подтверждения: {str(e)}"
        logger.exception(error_msg)
