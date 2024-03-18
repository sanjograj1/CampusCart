from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from .models import Event

EVENT_CATEGORY = [
    ("", "All"),
    ("Workshop", "Workshop"),
    ("Concert", "Concert"),
    ("Festival", "Festival"),
    ("Exhibition", "Exhibition"),
    ("Seminar", "Seminar"),
    ("Sports", "Sports"),
    ("Entertainment", "Entertainment"),
    ("Other", "Other"),
]

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'price','location','date_and_time','category', 'total_seats', 'image']
        widgets = {
            'date_and_time':forms.TextInput(attrs={'type':'datetime-local'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('price', css_class='form-control'),
            Field('location', css_class='form-control'),
            Field('date_and_time', css_class='form-control'),
            Field('category', css_class='form-control'),
            Field('total_seats', css_class='form-control'),
            Field('image', css_class='form-control')
        )

class EventFilterForm(forms.Form):
    category = forms.ChoiceField(
        choices=EVENT_CATEGORY, required=False, label="Category"
    )
