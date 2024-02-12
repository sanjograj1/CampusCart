from django import forms
from .models import Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone_number", "address", "profile_image"]


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
        if not email.endswith("@uwindsor.ca"):
            raise forms.ValidationError("Please enter a uwindsor.ca email")
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
