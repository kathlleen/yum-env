from django.contrib.auth.forms import UserChangeForm
from django import forms

from menu.models import Dish
from menu.models import Categories
from django.utils.text import slugify
from unidecode import unidecode


class DishForm(UserChangeForm):
    class Meta:
        model = Dish
        fields = ['image',
                  'name',
                  'description',
                  'price',
                  'discount',
                  'weight',
                  'category']

    image = forms.ImageField(required=False)
    name = forms.CharField()
    description = forms.CharField()
    price = forms.DecimalField(decimal_places=2, max_digits=7, initial=0.00)
    discount = forms.DecimalField(decimal_places=2, max_digits=7, initial=0.00)
    weight = forms.IntegerField()
    category = forms.ModelChoiceField(queryset=Categories.objects.all().order_by('name'), empty_label="(Nothing)")



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = ['name']

    def save(self, commit=True):
        category = super().save(commit=False)
        category.slug = slugify(unidecode(self.cleaned_data['name']))  # Генерируем slug из названия
        if commit:
            category.save()
        return category

