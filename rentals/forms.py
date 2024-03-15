from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from .models import Rental

class property_form(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['property_name','address_line1','address_line2','price','city','zip_code','state','country','description','property_image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('property_name', css_class='form-control'),
            Field('address_line1', css_class='form-control'),
            Field('address_line2', css_class='form-control'),
            Field('price', css_class='form-control'),
            Field('city', css_class='form-control'),
            Field('zip_code', css_class='form-control'),
            Field('state', css_class='form-control'),
            Field('country', css_class='form-control'),
            Field('description',css_class='form-control'),
            Field('property_image',css_class='form-control')
        )




    


