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


# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            existing_user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            existing_user = False
        if existing_user and not existing_user.is_active:
            messages.add_message(request, messages.ERROR, 'Please verify your account and try again!!',
                                 extra_tags='error-toast')
        else:
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')

            messages.add_message(request, messages.ERROR, 'Invalid credentials! Please try again',
                                 extra_tags='error-toast')
            if errors:
                return render(request, 'accounts/login.html', {
                    'page_title': 'Login',
                    'username': request.POST.get('username'),
                    'password': request.POST.get('password')
                })
    return render(request, 'accounts/login.html', {
        'page_title': 'Login',
        'username': '',
        'password': ''
    })


def sendemailverification(request, user, user_email):
    mail_subject = "Activate your user account."
    message = render_to_string("accounts/activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[user_email])
    if email.send():
        messages.add_message(request, messages.SUCCESS, f'Dear {user}, '
                                                        f'please go to you email {user_email} inbox and click on received activation '
                                                        f'link to confirm and complete the registration. Note: Check your spam folder.',
                             extra_tags='activate-toast')
    else:
        messages.add_message(request, messages.ERROR,
                             f'Problem sending email to {user_email}, check if you typed it correctly.',
                             extra_tags='error-toast')


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
                             extra_tags='success-toast')
        return redirect('login')
    else:
        messages.add_message(request, messages.SUCCESS,
                             "Activation link is invalid!",
                             extra_tags='error-toast')

    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_pic = request.FILES.get('profile_pic')

        errors = {}
        if not first_name:
            errors['first_name'] = 'Please enter your first name'
        if not last_name:
            errors['last_name'] = 'Please enter your last name'
        if not username:
            errors['username'] = 'Please enter your username'
        if not email.endswith('@uwindsor.ca'):
            errors['email'] = 'Please enter the uwindsor.ca email'

        if not password:
            errors['password'] = 'Please enter your password'
        else:
            if password != confirm_password:
                errors['confirm_password'] = 'Passport does not match'

        if not errors:
            if get_user_model().objects.filter(username=username).exists():
                errors['username'] = 'Username taken! Please try with a different username.'
                auth.logout(request)
            elif get_user_model().objects.filter(email=email).exists():
                errors['email'] = 'Email already exists! Please try a different email.'
                auth.logout(request)
            else:
                user = get_user_model().objects.create_user(first_name=first_name, last_name=last_name,
                                                            username=username,
                                                            password=password, email=email, is_active=False)
                user.save()
                sendemailverification(request, user, email)
                if profile_pic:
                    filename, ext = os.path.splitext(profile_pic.name)
                    filename = slugify(filename) + ext
                    user.profile_image.save(filename, ContentFile(profile_pic.read()), save=True)
                return redirect('login')
        else:
            return render(request, 'accounts/register.html',
                          {'email': email, 'email_error': errors.get('email', ''),
                           'confirm_password': confirm_password,
                           'confirm_password_error': errors.get('confirm_password', ''),
                           'first_name': first_name, 'first_error': errors.get('first_name', ''),
                           'last_name': last_name, 'last_error': errors.get('last_name', ''),
                           'password': password, 'password_error': errors.get('password', ''),
                           'username': username, 'username_error': errors.get('username', '')})

    return render(request, 'accounts/register.html',
                  {'email': '', 'email_error': '',
                   'confirm_password': '', 'confirm_password_error': '',
                   'first_name': '', 'first_error': '',
                   'last_name': '', 'last_error': '',
                   'username': '', 'username_error': '',
                   'password': '', 'password_error': ''})


@login_required(login_url='login')
def home(request):
    pic = request.user.profile_image
    context = {
        'page_title': 'Campus Cart',
        'profile': pic
    }
    return render(request, 'accounts/home.html', context)


def user_logout(request):
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, 'You have successfully logged out !!', extra_tags='success-toast')
    return redirect('login')
