from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from notifications.signals import notify

from .forms import EventForm
from .models import Event

@login_required
# Create your views here.
def eventshome(request):
    events = Event.objects.all()
    return render(request, 'events/eventshome.html',{
        'title': 'Events',
        'events':events
    })

@login_required
def eventdetail(request):
    return render(request, 'events/eventdetail.html',{
        'title': 'Event Detail',
    })


@login_required
def uploadevent(request):
    if request.method == 'POST':
        form = EventForm(request.POST,request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            sender = get_user_model().objects.get(username=request.user)
            receiver = get_user_model().objects.exclude(username=request.user)
            description = f'New Event Added - <b>{event.title}</b>. Click <a href="/events/event-detail/{event.id}">here</a> to view the upcoming event.'
            notify.send(sender, recipient=receiver, verb='Upload', description=description)
            return redirect('events:event-home')
    else:
        form = EventForm()
    return render(request,'events/upload_event.html',{'title': 'Upload Event','form':form})