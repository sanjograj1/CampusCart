import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Profile
from verify_email.email_handler import send_verification_email
from .forms import UserUpdateForm, ProfileUpdateForm, ProfileForm, RegistrationForm
from books.models import Book
from products.models import Product
from freestuff.models import FreeStuffItem


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


def register(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            inactive_user = send_verification_email(request, form)
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

    return render(request, "accounts/register.html", {
        "form": form,
        'title':'Register'
        })


@login_required
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
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your Profile has been updated")
            return redirect("accounts:profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "accounts/profile.html", {
        'user_form': user_form,
        'profile_form': profile_form,
        "title": "Profile",
    })


@login_required
def notifications_view(request):
    notifications = request.user.notifications.all()
    request.user.notifications.mark_all_as_read()
    return render(request, 'notifications.html', {
        'notifications': notifications,
        'title': 'Notifications'
    })


@login_required
def user_listing(request):
    user_books = Book.objects.filter(seller=request.user)
    user_free_items = FreeStuffItem.objects.filter(seller=request.user)
    user_products = Product.objects.filter(user=request.user)
    return render(request,'accounts/user_listing.html',{
        'user_books': user_books,
        'user_free_items': user_free_items,
        'user_products':user_products,
        'title':'My Listings'
    })