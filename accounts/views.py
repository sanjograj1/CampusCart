from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages


# Create your views here.
def login(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

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


def register(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

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

        if errors:
            return render(request, 'accounts/register.html',
                          {'email': email, 'email_error': errors.get('email', ''),
                           'confirm_password': confirm_password,
                           'confirm_password_error': errors.get('confirm_password', ''),
                           'first_name': first_name, 'first_error': errors.get('first_name', ''),
                           'last_name': last_name, 'last_error': errors.get('last_name', ''),
                           'password': password, 'password_error': errors.get('password', ''),
                           'username': username, 'username_error': errors.get('username', '')})

        if User.objects.filter(username=username).exists():
            errors['username'] = 'Username taken! Please try with a different username.'
        elif User.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists! Please try a different email.'
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                            password=password, email=email)
            user.save()
            return redirect('login')

    return render(request, 'accounts/register.html',
                  {'email': '', 'email_error': '',
                   'confirm_password': '', 'confirm_password_error': '',
                   'first_name': '', 'first_error': '',
                   'last_name': '', 'last_error': '',
                   'username': '', 'username_error': '',
                   'password': '', 'password_error': ''})

