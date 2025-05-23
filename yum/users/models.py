from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('customer', 'Customer'),
        ('restaurant_admin', 'Restaurant Admin'),
        ('courier', 'Courier'),
    )

    TRANSPORT_MODES = (
        ('foot', 'Пешком'),
        ('bicycle', 'На велосипеде'),
        ('scooter', 'На самокате'),
        ('motorcycle', 'На мотоцикле'),
        ('car', 'На машине'),
    )

    role = models.CharField(max_length=20, choices=USER_ROLES, default='customer')
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Изображение')
    latitude = models.FloatField(blank=True, null=True, verbose_name="Широта")  # Широта
    longitude = models.FloatField(blank=True, null=True, verbose_name="Долгота")  # Долгота
    liked_ingredients = models.TextField(blank=True, null=True,
                                         help_text="Что вы любите (например, сливки, сыр, грибы)")
    disliked_ingredients = models.TextField(blank=True, null=True,
                                            help_text="Что вы не любите (например, лук, каперсы)")

    transport_mode = models.CharField(
        max_length=20,
        choices=TRANSPORT_MODES,
        default='foot',
        verbose_name="Способ передвижения"
    )

    priority = models.FloatField(default=0.0, verbose_name="Приоритет")  # Обновляется программно

    def is_customer(self):
        return self.role == 'customer'

    def is_restaurant_admin(self):
        return self.role == 'restaurant_admin'

    def is_courier(self):
        return self.role == 'courier'
