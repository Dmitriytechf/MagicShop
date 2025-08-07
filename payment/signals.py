from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ShipingAdress


User = get_user_model()


@receiver(post_save, sender=User)
def create_default_shiping_address(sender, instance, created, **kwargs):
    '''
    При создании нового пользователя автоматически создаётся адрес доставки по умолчанию
    '''
    if created:
        if not ShipingAdress.objects.filter(user=instance).exists():
            ShipingAdress.create_default_shiping_address(user=instance)
