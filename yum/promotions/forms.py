# forms.py

from django import forms
from .models import PromotionRequest

class PromotionRequestForm(forms.ModelForm):
    class Meta:
        model = PromotionRequest
        fields = ['name', 'description', 'start_time', 'end_time', 'image']
