from django.contrib.auth.forms import UserChangeForm
from django import forms
import re
from menu.models import Dish, Label
from menu.models import Categories
from django.utils.text import slugify
from unidecode import unidecode

from restaurans.models import Restaurans


class DishForm(UserChangeForm):
    class Meta:
        model = Dish
        fields = ['image',
                  'name',
                  'description',
                  'price',
                  'discount',
                  'weight',
                  'category',
                  'composition',
                  'proteins',
                  'fats',
                  'carbohydrates',
                  'calories',
                  'labels']

    image = forms.ImageField(required=False)
    name = forms.CharField()
    description = forms.CharField()
    price = forms.DecimalField(decimal_places=2, max_digits=7, initial=0.00)
    discount = forms.IntegerField()
    weight = forms.IntegerField()
    category = forms.ModelChoiceField(queryset=Categories.objects.all().order_by('name'))
    composition = forms.CharField()
    proteins = forms.IntegerField()
    fats = forms.IntegerField()
    carbohydrates = forms.IntegerField()
    calories = forms.IntegerField()
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

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


class RestProfileForm(UserChangeForm):
    class Meta:
        model = Restaurans
        fields = ['image',
                  'name',
                  'description',
                  'address',
                  'phone_number']

    image = forms.ImageField(required=False)
    name = forms.CharField()
    description = forms.CharField()
    address = forms.CharField()
    phone_number = forms.CharField()

    def clean_phone_number(self): # валидация телефона
        data = self.cleaned_data['phone_number']
        #
        # if not data.isdigit():
        #     raise forms.ValidationError("Номер телефона должен содержать только цифры")

        pattern = re.compile(r'^(\+375|80)(29|25|44|33)(\d{3})(\d{2})(\d{2})$')
        if not pattern.match(data):
            raise forms.ValidationError("Неверный формат номера")

        return data