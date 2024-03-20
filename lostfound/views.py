from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LostandfoundItemForm
from django.contrib.auth import get_user_model

from notifications.signals import notify
from .models import LostandfoundItem


def laf_detail(request, post_id):
    post = get_object_or_404(LostandfoundItem, pk=post_id)

    return render(request, 'lostfound/post_detail.html', {'title': 'LostandFoundItem',
                                                          'post': post
    })

# def post(request):
#     if request.method == "POST":
#         form = LostandfoundItemForm(request.POST, request.FILES)

#         if form.is_valid():
#             form.save()
#             return redirect('home')

#         else:
#             form = LostandfoundItemForm()
        
#     return render(request,'lostfoundupload.html', {'form':form})

def index(request):
    posts = LostandfoundItem.objects.all()
    return render(request, 'lostfound/home.html',{
        'title': 'LostandFoundItems',
        'posts': posts
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
            description = f'Item has been uploaded - <b>{item.title}</b>'
            notify.send(sender, recipient=receiver, verb='Upload', description=description)
            return redirect('lostfound:upload')
    else:
        form = LostandfoundItemForm()
    return render(request,'lostfound/upload.html',{'title': 'Upload Post','form':form})

