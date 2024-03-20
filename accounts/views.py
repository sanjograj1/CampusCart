import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.models import auth
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate
from .models import Contact, UserComment, UserSession
from notifications.signals import notify
from verify_email.email_handler import send_verification_email
from .forms import (
    ContactForm,
    UserUpdateForm,
    ProfileUpdateForm,
    UserCommentsForm,
    RegistrationForm,
    LoginForm,
    ReportForm
)
from books.models import Book
from products.models import Product
from freestuff.models import FreeStuffItem
from rentals.models import Rental
from events.models import Event
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.forms import PasswordChangeForm



# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect("accounts:home")
    
    if request.method == "POST":
        form = LoginForm(None,data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                auth.login(request, user)
                return redirect("accounts:home")
        else:
            messages.add_message(
                    request,
                    messages.ERROR,
                    "Invalid credentials! Please try again",
                    extra_tags="danger",
                )        
    else:
        form = LoginForm()  
    return render(request,"accounts/login.html", {
        "title": "Login",
        "form":form
    })

import json

@login_required()
def profile_view(request, username):
    
    user = get_object_or_404(get_user_model(), username=username)
    comments = UserComment.objects.filter(user=user).order_by('-commented_date')
    address_dict = user.profile.address
    try:
        address_dict = user.profile.address
    except:
        address_dict = "Address does not exist"
        
    if request.method == "POST":
        if 'report' in request.POST:
            report_form = ReportForm(request.POST)
            if report_form.is_valid():
                report = report_form.save(commit=False)
                report.user = user
                report.reported_by = request.user
                report.save()
                messages.success(request, "Report has been submitted")
                return redirect("accounts:profile_view", username=username)
        else:
            comment_form = UserCommentsForm(request.POST)
            if comment_form.is_valid():
                form = comment_form.save(commit=False)
                form.commented_by = request.user
                form.user = user
                form.save()
                description = f'{request.user} added a new comnent on your profile Click <a href="/profile/rating/{user.username}">here</a> to view.'
                notify.send(request.user, recipient=user, verb='Comment', description=description)
                messages.success(request, "Your comment has been added")
                return redirect("accounts:profile_view", username=username)  
    else:
        report_form = ReportForm()
        comment_form = UserCommentsForm()
    return render(
        request,
        "accounts/profile_view.html",
        {
            "user": user,
            "address_dict": address_dict,
            "report_form": report_form,
            'comments':comments,
            'current_user': user,
            'title': f'{user.username} Rating',
            'comment_form':comment_form
        },
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("accounts:home")

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
        'title': 'Register'
    })


@login_required()
def home(request):
    # get all products sorted count of interested users
    products = Product.objects.filter(interested_users=request.user).order_by("-interested_users")
    current_viewed_books = request.COOKIES.get('viewed_books','')
    current_viewed_books = [int(book) for book in current_viewed_books.split(',') if book]
    viewed_books = Book.objects.filter(id__in=current_viewed_books)
    viewed_books = sorted(viewed_books, key=lambda x: current_viewed_books.index(x.id),reverse=True)

    current_viewed_properties = request.COOKIES.get('viewed_properties','')
    current_viewed_properties = [int(rental) for rental in current_viewed_properties.split(',') if rental]
    viewed_properties = Rental.objects.filter(id__in=current_viewed_properties)
    viewed_properties = sorted(viewed_properties, key=lambda x: current_viewed_properties.index(x.id),reverse=True)

    context = {
        "title": "Home",
        "products": products,
        'viewed_books':viewed_books,
        'viewed_properties':viewed_properties
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
        print("FILES", request.FILES)
        user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your Profile has been updated")
            return redirect("accounts:profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        # get address from profile form
        try:
            address_dict = request.user.profile.address
            address_dict = json.loads(address_dict)
            print("ADDRESS DICT", address_dict)
            coordinates = address_dict.get("coordinates")
            user_latitude = coordinates.get("latitude")
            user_longitude = coordinates.get("longitude")
            full_address = address_dict.get("full_address")
        except:
            user_latitude = 40.71669
            user_longitude = -73.961614
            full_address = ""

    return render(
        request,
        "accounts/profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "title": "Profile",
            "user_latitude": user_latitude,
            "full_address": full_address,
            "user_longitude": user_longitude,
        },
    )




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
    user_rentals = Rental.objects.filter(seller=request.user)
    user_events = Event.objects.filter(organizer=request.user)
    return render(
        request,
        "accounts/user_listing.html",
        {
            "user_books": user_books,
            "user_free_items": user_free_items,
            "user_products": user_products,
            "user_rentals": user_rentals,
            "user_events": user_events,
            "title": "My Listings",
        },
    )


@login_required
def toggle_sold_status(request, model, id):
    if model == "book":
        book = get_object_or_404(Book, pk=id)
        book.is_sold = not book.is_sold
        book.save()
        return redirect("accounts:user-listing")
    elif model == "freestuff":
        free_item = get_object_or_404(FreeStuffItem, pk=id)
        free_item.is_sold = not free_item.is_sold
        free_item.save()

    elif model == "product":
        product = get_object_or_404(Product, pk=id)
        product.is_sold = not product.is_sold
        product.save()

    elif model == "rental":
        rental = get_object_or_404(Rental, pk=id)
        rental.is_sold = not rental.is_sold
        rental.save()

    elif model == "event":
        event = get_object_or_404(Event, pk=id)
        event.is_sold = not event.is_sold
        event.save()

    else:
        return HttpResponse("Invalid Request")
    messages.success(request, "Status has been updated")
    return redirect("accounts:user-listing")



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
    return render(request, 'accounts/user_rating.html', {
        'comment_form': comment_form,
        'current_user': current_user,
        'title': f'{current_user.username.upper()} Rating',
        'comments': comments
    })


@login_required
def contactus(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():

            form.save()
            email = form.cleaned_data.get("email")
            # send email to user

            send_mail(
                "Contact Us",
                "We have received your request, we will get in touch with you soon.",
                settings.EMAIL_FROM,
                [email],
                fail_silently=False,
            )

            messages.info(request, "We'll get in touch with you soon.")
            return redirect("accounts:contactus")
    else:
        form = ContactForm(initial={"email": request.user.email,"name":request.user.first_name,"number":request.user.profile.phone_number})
    return render(request, "accounts/contactus.html", {"form": form})



@login_required
def login_history(request):
    all_history = UserSession.objects.filter(user=request.user).order_by('-created_at')
    one_day_ago = UserSession.objects.filter(user=request.user, created_at__gte=timezone.now() - timedelta(days=1))
    seven_day_ago = UserSession.objects.filter(user=request.user, created_at__gte=timezone.now() - timedelta(days=7))
    return render(request, 'accounts/login_history.html', {
        'all_history': all_history,
        'title': 'Login History',
        'one_day_ago': one_day_ago,
        'seven_day_ago': seven_day_ago
    })



@login_required
def change_theme(request):
    current_theme = request.COOKIES.get('theme', 'primary')
    response = HttpResponse("Setting Theme")
    
    if current_theme == 'primary':
        next_theme = 'secondary'
    else:
        next_theme = 'primary'
    response = redirect(request.META.get('HTTP_REFERER', '/'))
    response.set_cookie('theme', next_theme, max_age=5*24*60*60)
    
    return response

    # chnage password for user form
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Your password was successfully updated!")
            return redirect("accounts:profile")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/change_password.html", {"form": form})