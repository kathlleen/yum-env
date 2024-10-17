from django.contrib import admin

from orders.models import OrderItem, Order


# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    fields = [
        'user',
        'phone_number',
        'delivery_address',
        'slug',
        'payment_on_get',
        'is_paid',
        'status',
        'created_timestamp',
    ]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    fields = [
        'order',
        'dish',
        'name',
        'price',
        'quantity',
        'created_timestamp',
    ]