import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .tokens import account_activation_token
from .models import Profile, Contact
from verify_email.email_handler import send_verification_email
from .forms import UserUpdateForm, ProfileUpdateForm, ProfileForm, RegistrationForm


# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    errors = {}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            existing_user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            existing_user = False
        if existing_user and not existing_user.is_active:
            messages.add_message(
                request,
                messages.ERROR,
                "Please verify your account and try again!!",
                extra_tags="primary",
            )
        else:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("/")

            messages.add_message(
                request,
                messages.ERROR,
                "Invalid credentials! Please try again",
                extra_tags="danger",
            )
            if errors:
                return render(
                    request,
                    "accounts/login.html",
                    {
                        "title": "Login",
                        "username": request.POST.get("username"),
                        "password": request.POST.get("password"),
                    },
                )
    return render(
        request,
        "accounts/login.html",
        {"title": "Login", "username": "", "password": ""},
    )


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             "Thank you for your email confirmation. Now you can login your account.",
                             extra_tags='success')
        return redirect('login')
    else:
        messages.add_message(request, messages.SUCCESS,
                             "Activation link is invalid!",
                             extra_tags='danger')

    return redirect('accounts:login')


def register(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
            profile = Profile.objects.create(user=inactive_user)
            profile.save()
            messages.add_message(
            request,
            messages.SUCCESS,
            f"Dear {inactive_user}, "
            f"please go to you email {inactive_user.email} inbox and click on received activation "
            f"link to confirm and complete the registration. Note: Check your spam folder.",
            extra_tags="success",
        )
            return redirect("accounts:login")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required(login_url="login")
def home(request):
    context = {
        "title": "Campus Cart",
    }
    return render(request, "accounts/home.html", context)



def user_logout(request):
    auth.logout(request)
    messages.add_message(
        request,
        messages.SUCCESS,
        "You have successfully logged out !!",
        extra_tags="success",
    )
    return redirect("accounts:login")


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your Profile has been updated")
            return redirect("accounts:profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "accounts/profile.html",{
            'user_form' : user_form,
            'profile_form' : profile_form,
            "title": "Profile",
        })

@login_required
def contactus(request):
    print('Hi')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']
        contact = Contact(name=name, email=email, number=number)
        print('hello')
        contact.save()
        print('use created')
        messages.info(request, "We'll get in touch with you soon.")
    return render(request, 'accounts/contactus.html')