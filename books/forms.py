# forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'price','pages','language','category', 'book_cover']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('title', css_class='form-control'),
            Field('author', css_class='form-control'),
            Field('description', css_class='form-control'),
            Field('price', css_class='form-control'),
            Field('pages', css_class='form-control'),
            Field('language', css_class='form-control'),
            Field('category', css_class='form-control'),
            Field('book_cover', css_class='form-control'),
        )
