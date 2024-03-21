from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from .models import FreeStuffItem


class FreeItemForm(forms.ModelForm):
    class Meta:
        model = FreeStuffItem
        fields = ['title', 'description', 'quantity','category','condition', 'item_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('quantity', css_class='form-control'),
            Field('category', css_class='form-control'),
            Field('condition', css_class='form-control'),
            Field('item_image', css_class='form-control'),
        )

class FreeItemFiltersForm(forms.Form):
    CATEGORY_LIST = [
        ("", "----"),
        ("Electronics", "Electronics"),
        ("Clothing", "Clothing"),
        ("Shoes", "Shoes"),
        ("Furniture", "Furniture"),
        ("Others", "Others"),
    ]
    CONDITION_LIST = [
        ("", "----"),
        ("New", "New"),
        ("Used", "Used"),
    ]
    condition = forms.ChoiceField(
        choices=CONDITION_LIST, required=False, label="Condition"
    )
    category = forms.ChoiceField(
        choices=CATEGORY_LIST, required=False, label="Category"
    )