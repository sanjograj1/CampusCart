from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from .models import Rental

class property_form(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['property_name','address','price','city','zip_code','description','property_image']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('property_name', css_class='form-control'),
            Field('address', css_class='form-control'),
            Field('price', css_class='form-control'),
            Field('city', css_class='form-control'),
            Field('zip_code', css_class='form-control'),
            Field('description',css_class='form-control'),
            Field('property_image',css_class='form-control')
        )

SORT_BY_OPTIOS = [
    ('Newest','Newest'),
    ('Oldest','Oldest'),
    ('Lowest Price','Lower Price'),
    ('Highest Price','Highest Price'),
]

class PropertySearchForm(forms.Form):
    search=forms.CharField(max_length=250,required=False)
    sort_by = forms.ChoiceField(
        choices=SORT_BY_OPTIOS, required=False, label="Category"
    )

    


