from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse

from restaurans.models import Restaurans


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self): # перегружаем для отображения названия в бд
        return self.name

class Label(models.Model):
    TYPE_CHOICES = [
        ('universal', 'Универсальный'),
        ('diet', 'Диетический'),
        ('allergy', 'Аллергия'),
        ('preference', 'Предпочтение'),
    ]

    name = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    class Meta:
        verbose_name = 'Метку'
        verbose_name_plural = 'Метки'

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class Dish(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='dishes_images', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Скидка в %')
    weight = models.IntegerField(blank=True, null=True, verbose_name='Вес')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')
    restaurant = models.ForeignKey(to=Restaurans, blank=True, null=True, on_delete=models.CASCADE, related_name='restaurant', verbose_name='Ресторан')
    composition = models.TextField(blank=True)
    proteins = models.FloatField(null=True, blank=True)
    fats = models.FloatField(null=True, blank=True)
    carbohydrates = models.FloatField(null=True, blank=True)
    calories = models.FloatField(null=True, blank=True)
    labels = models.ManyToManyField(Label, through='DishLabel', related_name='dishes')


    # on_delete бывает:
    # - PROTECT (самый безопастный, не дает удалять,
    # - CASCADE (удаляются и все товары, закрепленные за категорией (с предупреждением))
    # - SET_DEFAULT (всем товарам присвоено default value)
    class Meta:
        db_table = 'dish'
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering: ("id",)

    def __str__(self):
        return f'{self.name}'

    def display_id(self):
        return f'{self.id:05}'

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        else:
            return self.price

    # def get_absolute_url(self):
    #     return reverse("catalog:product", kwargs={"product_slug":self.slug})

class DishLabel(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('dish', 'label')

    def __str__(self):
        return f"{self.dish.name} - {self.label.name}"