# forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from .models import LostandfoundItem

class LostandfoundItemForm(forms.ModelForm):
    class Meta:
        model = LostandfoundItem
        fields = ['category', 'title', 'product_description', 'post_date','image','location']

        
    