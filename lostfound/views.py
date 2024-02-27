from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


@login_required
def index(request):
    return render(request, 'lostfound/home.html', {
        'title': 'Lost & Found'
    })