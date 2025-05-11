from django.db import models
from restaurans.models import Restaurans

# Create your models here.
class Selection(models.Model):
    name = models.CharField(max_length=60, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(null=True, blank=True, verbose_name="Описание")
    image = models.ImageField(upload_to='collections_images', blank=True, null=True, verbose_name='Изображение')
    restaurants = models.ManyToManyField(
        Restaurans,
        through='SelectionRestaurant',
        related_name='selections',
        verbose_name="Рестораны"
    )
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'restCollections'
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

    def __str__(self):
        return f'{self.name}'

class SelectionRestaurant(models.Model):
    selection = models.ForeignKey(Selection, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurans, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('selection', 'restaurant')
        verbose_name = "Ресторан в подборке"
        verbose_name_plural = "Рестораны в подборках"

    def __str__(self):
        return f"{self.restaurant.name} в «{self.selection.name}»"