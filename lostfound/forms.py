from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from .models import LostandfoundItem

class LostandfoundItemForm(forms.ModelForm):
    
    class Meta:
        model = LostandfoundItem
        fields = ['category', 'title', 'product_description', 'image','location']
        
        # widgets = {
        #     'date_and_time':forms.TextInput(attrs={'type':'datetime-local'}),
        # }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('category', css_class='form-control'),
            Field('title', css_class='form-control'),
            Field('product_description', css_class='form-control'),
            Field('image', css_class='form-control'),
            Field('location', css_class='form-control'),
        )
