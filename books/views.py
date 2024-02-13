from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required()
# Create your views here.
def furniture(request):
    return render(request, 'books/home.html',{
        'page_title': 'Books',
    })