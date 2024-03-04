import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect,reverse
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Profile, UserComment, Contact
from notifications.signals import notify
from verify_email.email_handler import send_verification_email
from .forms import UserUpdateForm, ProfileUpdateForm, UserCommentsForm, RegistrationForm, ContactForm
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

@login_required()
def home(request):

    # get all products sorted count of interested users
    products = Product.objects.all().order_by("-interested_users")[:4]
    context = {
        "title": "Campus Cart",
        "products": products,
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


@login_required
def user_rating(request, username):
    current_user = get_object_or_404(get_user_model(), username=username)
    comments = UserComment.objects.filter(user=current_user).order_by('-commented_date')
    if request.method == 'POST':
        comment_form = UserCommentsForm(request.POST)
        if comment_form.is_valid():
            form = comment_form.save(commit=False)
            form.commented_by = request.user
            form.user = current_user
            form.save()
            description = f'{request.user} added a new comnent on your profile Click <a href="/profile/rating/{current_user.username}">here</a> to view.'
            notify.send(request.user, recipient=current_user, verb='Comment', description=description)
            messages.success(request, "Your comment has been added")
            url = reverse('accounts:user-rating', args=[username])
            return redirect(url)
    else:
        comment_form = UserCommentsForm()
    return render(request,'accounts/user_rating.html',{
        'comment_form':comment_form,
        'current_user':current_user,
        'title': f'{current_user.username.upper()} Rating',
        'comments':comments
    })

@login_required
def contactus(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            number = form.cleaned_data['phone_number']

            contact = Contact.objects.create(name=name, email=email, number=number)

        
            messages.info(request, "We'll get in touch with you soon.")
            return redirect('accounts:contactus')
    else:
        form = ContactForm()
    return render(request, 'accounts/contactus.html', {'form': form})