from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('customer', 'Customer'),
        ('restaurant_admin', 'Restaurant Admin'),
        ('courier', 'Courier'),
    )

    role = models.CharField(max_length=20, choices=USER_ROLES, default='customer')
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Изображение')
    latitude = models.FloatField(blank=True, null=True, verbose_name="Широта")  # Широта
    longitude = models.FloatField(blank=True, null=True, verbose_name="Долгота")  # Долгота
    liked_ingredients = models.TextField(blank=True, null=True,
                                         help_text="Что вы любите (например, сливки, сыр, грибы)")
    disliked_ingredients = models.TextField(blank=True, null=True,
                                            help_text="Что вы не любите (например, лук, каперсы)")

    def is_customer(self):
        return self.role == 'customer'

    def is_restaurant_admin(self):
        return self.role == 'restaurant_admin'

    def is_courier(self):
        return self.role == 'courier'
