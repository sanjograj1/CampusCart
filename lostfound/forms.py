from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from .models import LostandfoundItem

class LostandfoundItemForm(forms.ModelForm):
    
    class Meta:
        model = LostandfoundItem
        fields = ['category', 'title', 'product_description', 'image','location']
    
    
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
        self.fields['location'].help_text = 'Please provide the exact location'

class ItemFilter(forms.Form):
    ITEM_CATEGORY = [
        ("", "----"),
        ("LOST", "Lost"),
        ("FOUND", "Found"),
    ]
    name = forms.CharField(label="Item Name",required=False)
    category = forms.ChoiceField(
        choices=ITEM_CATEGORY, required=False, label="Category"
    )