from django.contrib import admin
from .models import Selection, SelectionRestaurant

class SelectionRestaurantInline(admin.TabularInline):
    model = SelectionRestaurant
    extra = 1

@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    inlines = [SelectionRestaurantInline]

    prepopulated_fields = {'slug': ('name',)}
