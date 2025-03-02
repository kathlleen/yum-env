from django.contrib import admin

from restaurans.models import Cuisine, Restaurans
from restaurans.utils import get_coordinates


# Register your models here.

class RestauransTabAdmin(admin.TabularInline):
    model = Restaurans
    fields = ["name"]
    search_fields = ["name"]
    extra = 1
@admin.register(Restaurans)
class RestauransAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

    def save_model(self, request, obj, form, change):
        if "address" in form.changed_data:  # Если адрес изменился
            obj.latitude, obj.longitude = get_coordinates(obj.address)
        super().save_model(request, obj, form, change)


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}