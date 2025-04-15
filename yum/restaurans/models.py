from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, time, timedelta
from django.utils import timezone
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

    start_time = models.TimeField(blank=True, null=True,verbose_name="Начало работы")
    end_time = models.TimeField(blank=True, null=True, verbose_name="Конец работы")

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

    def is_open(self):
        if not self.start_time or not self.end_time:
            return False  # если время не указано — считаем закрытым

        now = timezone.localtime().time()
        if self.start_time < self.end_time:
            return self.start_time <= now <= self.end_time
        else:
            # ночной режим (например, с 22:00 до 02:00)
            return now >= self.start_time or now <= self.end_time

    def closes_soon(self, minutes=30):
        if not self.end_time:
            return False

        now = timezone.localtime()
        end_dt = datetime.combine(now.date(), self.end_time)

        if self.start_time > self.end_time:
            end_dt += timedelta(days=1)  # ночной режим

        # Сделать end_dt aware
        end_dt = timezone.make_aware(end_dt, timezone.get_current_timezone())

        return timedelta(0) <= (end_dt - now) <= timedelta(minutes=minutes)


