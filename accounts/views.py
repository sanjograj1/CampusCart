import os

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.text import slugify
from accounts.forms import ProfileForm, RegistrationForm
from accounts.models import Profile
from verify_email.email_handler import send_verification_email


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
                extra_tags="error-toast",
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
                extra_tags="error-toast",
            )
            if errors:
                return render(
                    request,
                    "accounts/login.html",
                    {
                        "page_title": "Login",
                        "username": request.POST.get("username"),
                        "password": request.POST.get("password"),
                    },
                )
    return render(
        request,
        "accounts/login.html",
        {"page_title": "Login", "username": "", "password": ""},
    )


def sendemailverification(request, user, user_email):
    mail_subject = "Activate your user account."
    message = render_to_string(
        "accounts/activate_account.html",
        {
            "user": user.username,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http",
        },
    )
    email = EmailMessage(mail_subject, message, to=[user_email])
    if email.send():
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Dear {user}, "
            f"please go to you email {user_email} inbox and click on received activation "
            f"link to confirm and complete the registration. Note: Check your spam folder.",
            extra_tags="activate-toast",
        )
    else:
        messages.add_message(
            request,
            messages.ERROR,
            f"Problem sending email to {user_email}, check if you typed it correctly.",
            extra_tags="error-toast",
        )


def register(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():

            inactive_user = send_verification_email(request, form)

            profile = Profile.objects.create(user=inactive_user)
            profile.save()
            messages.success(request, "registered Successfully")

            return redirect("accounts:login")
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required(login_url="login")
def home(request):
    pic = request.user.profile_image
    context = {"page_title": "Campus Cart", "profile": pic}
    return render(request, "accounts/home.html", context)


def user_logout(request):
    auth.logout(request)
    messages.add_message(
        request,
        messages.SUCCESS,
        "You have successfully logged out !!",
        extra_tags="success-toast",
    )
    return redirect("accounts:login")


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, "accounts/profile.html", {"form": form})
