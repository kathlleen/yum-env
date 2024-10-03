from django.contrib import admin

from restaurans.models import Cuisine

# Register your models here.
# admin.site.register(Cuisine)

@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name',)}