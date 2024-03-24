from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LostandfoundItemForm, ItemFilter
from django.contrib.auth import get_user_model
from django.contrib import messages


from notifications.signals import notify
from .models import LostandfoundItem
import requests


def laf_detail(request, post_id):
    post = get_object_or_404(LostandfoundItem, pk=post_id)  
    myAPIKey = 'c20c43b8dddc42939c4304857ea1ce69'
    print(post.location)
    url = f"https://api.geoapify.com/v1/geocode/search?text={post.location}&limit=1&apiKey={myAPIKey}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result = data["features"][0]
        print(result)
        userlatitude = result["geometry"]["coordinates"][1]
        userlongitude = result["geometry"]["coordinates"][0]
    else:
        print(f"Request failed with status code {response.status_code}")
    
    return render(request, 'lostfound/post_detail.html',{
        'title': 'LostandFoundItem',
        'post': post,
        'userlatitude':userlatitude,
        'userlongitude':userlongitude
    })


@login_required
def index(request):
    if request.method == 'GET':
        form = ItemFilter(request.GET)
        if form.is_valid():
            item_name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            items  = LostandfoundItem.objects.all()
            if category:
                items = items.filter(category=category)
            if item_name:
                items = items.filter(title__contains=item_name)

    else:
        items = LostandfoundItem.objects.all()
    return render(request, 'lostfound/home.html', {
        'title': 'Items',
        'items': items,
        'form': form,
    })


@login_required
def post(request):
    if request.method == 'POST':
        form = LostandfoundItemForm(request.POST,request.FILES)
        if form.is_valid():
            item  = form.save(commit=False)
            item.user = request.user
            item.save()
            sender = get_user_model().objects.get(username=request.user)
            receiver = get_user_model().objects.exclude(username=request.user)
            description = f'<b>{item.title}</b> (Lost & Found Item). Click <a href="/lostandfound/post_detail/{item.id}">here</a> to view.'
            notify.send(sender, recipient=receiver, verb='Upload', description=description)
            return redirect('lostfound:home')
    else:
        form = LostandfoundItemForm()
    return render(request,'lostfound/upload.html',{'title': 'Upload Post','form':form})

@login_required
def editpost(request, postid):
    my_post = get_object_or_404(LostandfoundItem, pk=postid)
    if my_post.user != request.user:
        messages.success(request, "You don't have the access to the Post", extra_tags='danger')
        return redirect('accounts:user-listing')
    if request.method == 'POST':
        if 'action' in request.POST:
            form = LostandfoundItemForm(request.POST, request.FILES, instance=my_post)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
                return redirect('accounts:user-listing')
        else:
            my_post.delete()
            messages.success(request, "Your Post has been deleted", extra_tags='danger')
            return redirect('accounts:user-listing')
    else:
        form = LostandfoundItemForm(instance=my_post)
    return render(request, 'lostfound/edit_post.html', {
        'form': form,
        'title': 'Edit Post'
    })