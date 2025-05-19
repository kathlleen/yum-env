from django.contrib import admin

from menu.models import Categories, Dish, DishLabel, Label, LabelPreference


# Register your models here.
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class DishLabelInline(admin.TabularInline):
    model = DishLabel
    extra = 1

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    list_filter = ('type',)
    search_fields = ('name',)

@admin.register(LabelPreference)
class LabelPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'label', 'preference_type')
    list_filter = ('label', 'preference_type',)
    search_fields = ('label', 'preference_type',)


@admin.register(Dish)
class DishesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id', 'name', 'price', 'discount', 'restaurant']
    list_editable = ['discount']
    search_fields = ['name', 'description', 'restaurant']
    list_filter = ['category', 'discount', 'restaurant']
    inlines = [DishLabelInline]
    fields = [
        'name',
        'category',
        'restaurant',
        'slug',
        'description',
        'image',
        ('price', 'discount'),
        'weight',
        'composition',
        'proteins',
        'fats',
        'carbohydrates',
        'calories',
    ]