from django.contrib import admin
from couriers.models import Shift


# Register your models here.
@admin.register(Shift)
class CartAdmin(admin.ModelAdmin):
    list_display = ['courier','start_time', 'end_time', 'duration']

