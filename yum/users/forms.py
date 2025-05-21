from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
import re
from menu.models import Label, LabelPreference
from users.models import CustomUser


class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class ProfileForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['image',
                  'first_name',
                  'last_name',
                  'username',
                  'email']

    image = forms.ImageField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()

    # def clean_email(self): # валидация телефона
    #     data = self.cleaned_data['email']
    #     #
    #     # if not data.isdigit():
    #     #     raise forms.ValidationError("Номер телефона должен содержать только цифры")
    #
    #     pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    #     if not pattern.match(data):
    #         raise forms.ValidationError("Неверный формат почты")
    #
    #     return data

    def clean_phone_number(self): # валидация телефона
        data = self.cleaned_data['phone_number']
        #
        # if not data.isdigit():
        #     raise forms.ValidationError("Номер телефона должен содержать только цифры")

        pattern = re.compile(r'^(\+375|80)(29|25|44|33)(\d{3})(\d{2})(\d{2})$')
        if not pattern.match(data):
            raise forms.ValidationError("Неверный формат номера")

        return data


class UserPreferenceForm(forms.ModelForm):
    like_labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.filter(type='universal'),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Нравятся'
    )
    dislike_labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.filter(type='universal'),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Не нравятся'
    )
    diet_labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.filter(type='diet'),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Диеты'
    )
    allergy_labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.filter(type='allergy'),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Аллергии'
    )

    class Meta:
        model = CustomUser
        fields = ['liked_ingredients', 'disliked_ingredients']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

        # Загружаем текущие предпочтения
        for pref_type in ['like', 'dislike', 'diet', 'allergy']:
            field_name = f'{pref_type}_labels'
            selected = LabelPreference.objects.filter(user=user, preference_type=pref_type).values_list('label_id', flat=True)
            self.fields[field_name].initial = selected




class CustomerRegistrationForm(UserCreationForm):

    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'password1',
                  'password2'
                  ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'  # Устанавливаем роль покупателя
        if commit:
            user.save()
        return user

class RestaurantAdminRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'restaurant_admin'  # Устанавливаем роль администратора ресторана
        if commit:
            user.save()
        return user


class CourierRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'password1',
                  'password2'
                  ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'courier'  # Устанавливаем роль курьера
        if commit:
            user.save()
        return user