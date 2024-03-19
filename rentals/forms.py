from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import Rental


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['property_name', 'address', 'price', 'city', 'zip_code', 'description', 'property_image', 'bedrooms', 'bathrooms', 'furnished',
                  'agreement', 'appliances', 'description', 'parking']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('property_name', css_class='form-control'),
            Field('address', css_class='form-control'),
            Field('price', css_class='form-control'),
            Field('city', css_class='form-control'),
            Field('zip_code', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('property_image', css_class='form-control'),
            Field('bedrooms', css_class='form-control'),
            Field('bathrooms', css_class='form-control'),
            Field('furnished', css_class='form-control'),
            Field('agreement', css_class='form-control'),
            Field('appliances', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('parking', css_class='form-control')
        )
        self.fields['address'].help_text = 'Please provide the complete address'
        self.fields['agreement'].help_text = 'Please provide the lease in months'



class PropertySearchForm(forms.Form):
    SORT_BY_OPTIONS = [
        ('Newest', 'Newest'),
        ('Oldest', 'Oldest'),
        ('Lowest Price', 'Lower Price'),
        ('Highest Price', 'Highest Price'),
    ]
    search = forms.CharField(max_length=250, required=False)
    sort_by = forms.ChoiceField(
        choices=SORT_BY_OPTIONS, required=False, label="Sort By"
    )
