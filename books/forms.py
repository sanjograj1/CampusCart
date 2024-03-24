# forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'price', 'pages', 'language', 'category','condition', 'book_cover']

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


class BooksFilter(forms.Form):
    BOOKS_CATEGORY = [
        ("", "----"),
        ("Fiction", "Fiction"),
        ("Non-Fiction", "Non-Fiction"),
        ("Academic", "Academic"),
        ("Children", "Children"),
        ("Art & Photography", "Art & Photography"),
        ("Cookbooks", "Cookbooks"),
        ("Travel", "Travel"),
        ("Health & Wellness", "Health & Wellness"),
        ("Religion & Spirituality", "Religion & Spirituality"),
        ("Hobbies & Crafts", "Hobbies & Crafts"),
        ("Sports & Recreation", "Sports & Recreation"),
        ("Science Fiction & Fantasy", "Science Fiction & Fantasy"),
        ("Horror", "Horror"),
        ("Poetry", "Poetry"),
        ("Drama", "Drama"),
        ("Others", "Others"),
    ]
    PRICE_RANGE = [
        ("", "----"),
        ("0-10", "$0-10"),
        ("10-20", "$10-20"),
        ("20-30", "$20-30"),
        ("30-40", "$30-40"),
        ("40-50", "$40-50"),
        ("50-1000", "$50 or More"),
    ]
    name = forms.CharField(label="Book Name",required=False)
    category = forms.ChoiceField(
        choices=BOOKS_CATEGORY, required=False, label="Category"
    )
    price = forms.ChoiceField(choices=PRICE_RANGE, required=False, label="Price Range")
