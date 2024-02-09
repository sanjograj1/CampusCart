from django.shortcuts import render


# Create your views here.
def login(request):
    return render(request, 'accounts/login.html')


def register(request):
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
    return render(request, 'accounts/register.html',
                  {'email': '', 'email_error': '',
                   'confirm_password': '', 'confirm_password_error': '',
                   'first_name': '', 'first_error': '',
                   'last_name': '', 'last_error': '',
                   'username': '', 'username_error': '',
                   'password': '', 'password_error': ''})
