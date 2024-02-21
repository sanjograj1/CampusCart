from django.shortcuts import render
from .models import FreeStuffItem

def index(request):
    items = FreeStuffItem.objects.all()
    return render(request, 'freestuff/home.html', {
        'items': items,
        'title':'Free Stuff'
    })