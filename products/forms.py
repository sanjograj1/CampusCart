from django import forms
from .models import Product
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.helper import FormHelper

CATEGORY_LIST = [
    ("", "All"),
    ("Electronics", "Electronics"),
    ("Clothing", "Clothing"),
    ("Shoes", "Shoes"),
    ("Books", "Books"),
    ("Furniture", "Furniture"),
    ("Others", "Others"),
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "price", "image", "category"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("title", css_class="form-control"),
            Field("description", css_class="form-control"),
            Field("price", css_class="form-control"),
            Field("image", css_class="form-control"),
        )


class ProductFilterForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)
    category = forms.ChoiceField(
        choices=CATEGORY_LIST, required=False, label="Category"
    )
