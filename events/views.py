from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
# Create your views here.
def eventshome(request):
    return render(request, 'events/eventshome.html',{
        'title': 'Events',
    })

@login_required
def eventdetail(request):
    return render(request, 'events/eventdetail.html',{
        'title': 'Event Detail',
    })