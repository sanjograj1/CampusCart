from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import FreeItemForm
from .models import FreeStuffItem


@login_required
def index(request):
    items = FreeStuffItem.objects.all()
    return render(request, 'freestuff/home.html', {
        'items': items,
        'title': 'Free Stuff'
    })


@login_required
def upload_item(request):
    if request.method == 'POST':
        form = FreeItemForm(request.POST, request.FILES)
        if form.is_valid():
            free_item = form.save(commit=False)
            free_item.seller = request.user
            free_item.save()
            return redirect('freestuff:home')
    else:
        form = FreeItemForm()
    return render(request, 'freestuff/upload_item.html', {
        'form': form,
        'title':'Upload your Item'
        })


@login_required
def item_detail(request, itemid):
    current_item = get_object_or_404(FreeStuffItem, pk=itemid)
    return render(request, 'freestuff/item_detail.html',{
        'title':current_item.title,
        'item':current_item,
    })