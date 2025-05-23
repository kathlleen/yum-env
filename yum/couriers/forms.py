from django import forms
from django.contrib.auth.forms import UserChangeForm
import re
from users.models import CustomUser


class CourierProfileForm(UserChangeForm):
    TRANSPORT_CHOICES = CustomUser.TRANSPORT_MODES

    image = forms.ImageField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    phone_number = forms.CharField(required=False)
    transport_mode = forms.ChoiceField(choices=TRANSPORT_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = [
            'image',
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'transport_mode'
        ]

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if data:
            pattern = re.compile(r'^(\+375|80)(29|25|44|33)(\d{3})(\d{2})(\d{2})$')
            if not pattern.match(data):
                raise forms.ValidationError("Неверный формат номера")
        return data
