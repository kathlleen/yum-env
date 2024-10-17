from django.db import models

from restaurans.models import Restaurans


# Create your models here.
class Promotion(models.Model):
    restaurant = models.ForeignKey(to=Restaurans, on_delete=models.CASCADE, verbose_name="Ресторан")
    name = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(max_length=200, verbose_name="Описание акции")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата начала акции")
    end_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата конца акции")

    class Meta:
        db_table = "promotion"
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

    def __str__(self):
        return f"Акция {self.name} | Ресторан {self.restaurant.name}"