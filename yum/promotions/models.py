from django.db import models

from restaurans.models import Restaurans


# Create your models here.\

class PromotionRequest(models.Model):
    restaurant = models.ForeignKey(to=Restaurans, on_delete=models.CASCADE, verbose_name="Ресторан")
    name = models.CharField(max_length=50, verbose_name="Название акции")
    description = models.TextField(max_length=500, verbose_name="Описание")
    start_time = models.DateField(verbose_name="Дата начала")
    end_time = models.DateField(verbose_name="Дата конца")
    image = models.ImageField(upload_to='promotion_request_images', blank=True, null=True, verbose_name="Изображение")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    is_approved = models.BooleanField(default=False, verbose_name="Одобрено админом")
    is_active = models.BooleanField(default=False, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Заявка на акцию"
        verbose_name_plural = "Заявки на акции"

    def __str__(self):
        return f"Заявка на акцию {self.name} | {self.restaurant.name}"


class Promotion(models.Model):
    restaurant = models.ForeignKey(to=Restaurans, on_delete=models.CASCADE, verbose_name="Ресторан")
    name = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(max_length=200, verbose_name="Описание акции")
    start_time = models.DateField(verbose_name="Дата начала акции")
    end_time = models.DateField(verbose_name="Дата конца акции")
    image = models.ImageField(upload_to='promotion_images', blank=True, null=True, verbose_name='Изображение')

    class Meta:
        db_table = "promotion"
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

    def __str__(self):
        return f"Акция {self.name} | Ресторан {self.restaurant.name}"