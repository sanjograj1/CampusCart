from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from notifications.signals import notify
from django.utils import timezone

from .forms import EventForm, EventFilterForm
from .models import Event

@login_required
def eventshome(request):
    today = timezone.now()
    two_weeks = today + timezone.timedelta(weeks=2)
    upcomingevents = Event.objects.filter(date_and_time__range=[today, two_weeks])
    
    categories = Event.objects.values_list('category', flat=True).distinct()
    if request.method == 'GET':
        form = EventFilterForm(request.GET)
        if form.is_valid():
            all_categories = form.cleaned_data.get("category")
            if all_categories:          
                events = Event.objects.filter(category=all_categories)
            else:
                events = Event.objects.all()
    else:
        events = Event.objects.all()

    return render(request, 'events/eventshome.html',{
        'title': 'Events',
        'events': events,
        'upcoming_events': upcomingevents,
        'form': form,
    })

@login_required
def eventdetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'events/eventdetail.html',{
        'title': 'Event Detail',
        'event': event,
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
