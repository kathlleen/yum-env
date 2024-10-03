# from django.contrib.auth.models import AbstractUser
from django.db import models


#
# # Create your models here.
# class Restaurans(AbstractUser):
#     name = models.CharField(max_length=60, verbose_name="Название")
#     slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, verbose_name='URL')
#     address = models.TextField(null=True, blank=True, verbose_name="Адрес")
#     phone_number = models.CharField(max_length=20, verbose_name="Контактный телефон")
#
#
#     class Meta:
#         db_table = 'restaurans'
#         verbose_name = 'Ресторан'
#         verbose_name_plural = 'Рестораны'
#
#     def __str__(self):
#         return f'{self.name}'

class Cuisine(models.Model):
    name = models.CharField(max_length=60, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'cuisine'
        verbose_name = 'Кухня'
        verbose_name_plural = 'Кухни'

    def __str__(self):
        return f'{self.name}'
