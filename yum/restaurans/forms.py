from django.contrib.auth.forms import UserChangeForm
from django import forms

from menu.models import Dish
from menu.models import Categories


class DishEditForm(UserChangeForm):
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
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), empty_label="(Nothing)")




