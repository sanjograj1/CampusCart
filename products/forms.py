from django import forms
from .models import Product
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.helper import FormHelper


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "price", "image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('price', css_class='form-control'),
            Field('image', css_class='form-control'),
        )     