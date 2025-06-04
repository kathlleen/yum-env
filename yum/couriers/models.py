from django.db import models
from django.utils import timezone
from users.models import CustomUser
from decimal import Decimal
from orders.models import Order


# Create your models here.
class Shift(models.Model):
    courier = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="shifts")
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(blank=True, null=True)

    def is_active(self):
        return self.end_time is None

    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return timezone.now() - self.start_time

    def total_earnings(self):
        completed_orders = Order.objects.filter(
            courier=self.courier,
            status='delivered',
            created_timestamp__range=(self.start_time, self.end_time or timezone.now())
        )
        total = 0
        for order in completed_orders:
            total += sum(item.price * item.quantity for item in order.orderitem_set.all())

        return total * Decimal('0.05')  # 5% курьеру

    class Meta:
        verbose_name = "Смена"
        verbose_name_plural = "Смены"
        ordering = ['-start_time']
