from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

def laf_detail(request):
    return render(request, 'lostfound/post_detail.html')

@login_required
def index(request):
    return render(request, 'lostfound/home.html', {
        'title': 'Lost & Found'
    })

