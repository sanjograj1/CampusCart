from django import forms
from .models import Profile, UserComment
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.layout import Layout, Submit, Field
from crispy_forms.helper import FormHelper
from PIL import Image
from django.conf import settings


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone_number", "address", "profile_image"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('phone_number', css_class='form-control'),
            Field('address', css_class='form-control'),
            Field('profile_image', css_class='form-control'),
        )    

    def save(self):
        super.save()  

        img = Image.open(self.profile_image.path)
        if img.height > 400 and img.width > 400:
            output_size = (400,400)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email.endswith(settings.EMAIL_VERIFY):
            raise forms.ValidationError(f'Please enter a {settings.EMAIL_VERIFY} mail')
        elif get_user_model().objects.filter(email=email).exists():
                raise forms.ValidationError('Email already exists! Please try a different email.')
        return email
    

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username', css_class='form-control'),
            Field('email', css_class='form-control'),
            Field('first_name', css_class='form-control'),
            Field('last_name', css_class='form-control'),
        ) 
        self.fields['username'].disabled = True 
        self.fields['email'].disabled = True
        self.fields['username'].help_text = 'Cannot Change Username again'
        self.fields['email'].help_text = 'Cannot Change Email again'

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number','address','profile_image']       

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('phone_number', css_class='form-control'),
            Field('address', css_class='form-control'),
            Field('profile_image', css_class='form-control'),
        )

class UserCommentsForm(forms.ModelForm):

    class Meta:
        model = UserComment
        fields = ['comment']  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('comment', css_class='form-control'),
        )         



class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name')
    email = forms.EmailField(label='Email')
    phone_number = forms.CharField(max_length=15, label='Phone Number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name', css_class='form-control'),
            Field('email', css_class='form-control'),
            Field('phone_number', css_class='form-control'),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )