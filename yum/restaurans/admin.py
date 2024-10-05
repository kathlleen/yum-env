from django.contrib import admin

from restaurans.models import Cuisine, Restaurans

# Register your models here.

class RestauransTabAdmin(admin.TabularInline):
    model = Restaurans
    fields = ["name"]
    search_fields = ["name"]
    extra = 1
@admin.register(Restaurans)
class RestauransAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}