from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from restaurans.utils import get_coordinates


# Create your models here.

class Cuisine(models.Model):
    name = models.CharField(max_length=60, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'cuisine'
        verbose_name = 'Кухня'
        verbose_name_plural = 'Кухни'

    def __str__(self):
        return f'{self.name}'
class Restaurans(models.Model):
    name = models.CharField(max_length=60, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, verbose_name='URL')
    address = models.TextField(null=True, blank=True, verbose_name="Адрес")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    rating = models.FloatField(null=True, verbose_name="Рейтинг (звезды)")
    phone_number = models.CharField(null=True, blank=True, max_length=20, verbose_name="Контактный телефон")
    image = models.ImageField(upload_to='restaurants_images', blank=True, null=True, verbose_name='Изображение')
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='restaurant', verbose_name='Админ')
    cuisine = models.ForeignKey(to=Cuisine, blank=True, on_delete=models.SET_NULL, null=True, verbose_name="Кухня")
    latitude = models.FloatField(blank=True, null=True, verbose_name="Широта")  # Широта
    longitude = models.FloatField(blank=True, null=True, verbose_name="Долгота")  # Долгота

    class Meta:
        db_table = 'restaurans'
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self.address and (self.latitude is None or self.longitude is None):
            self.latitude, self.longitude = get_coordinates(self.address)
        super().save(*args, **kwargs)



