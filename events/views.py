from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render, get_object_or_404
from notifications.signals import notify
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.paginator import Paginator

from .forms import EventForm, EventFilterForm
from .models import Event
import pytz

@login_required
def eventshome(request):
    
    categories = Event.objects.values_list('category', flat=True).distinct()
    if request.method == 'GET':
        form = EventFilterForm(request.GET)
        if form.is_valid():
            all_categories = form.cleaned_data.get("category")
            if all_categories:          
                events = Event.objects.filter(category=all_categories)
            else:
                events = Event.objects.all()

            paginator = Paginator(events, 9)

            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)    
    else:
        events = Event.objects.all()

    return render(request, 'events/eventshome.html',{
        'title': 'Events',
        'events': events,
        'form': form,
        'page_obj':page_obj
    })


@login_required
def eventdetail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    today = timezone.now()
    two_weeks = today + timezone.timedelta(weeks=2)
    upcomingevents = Event.objects.filter(date_and_time__range=[today, two_weeks])
    remaining_time = event.date_and_time - timezone.now()
    if remaining_time.total_seconds() < 0:
        remaining_time_str = "Event has passed"
    else:
        remaining_days = remaining_time.days
        remaining_hours = remaining_time.seconds // 3600
        remaining_minutes = (remaining_time.seconds // 60) % 60
        remaining_seconds = remaining_time.seconds % 60
        remaining_time_str = {
            'days': remaining_days,
            'hours': remaining_hours,
            'minutes': remaining_minutes,
            'seconds': remaining_seconds
        }

    return render(request, 'events/eventdetail.html', {
        'title': 'Event Detail',
        'event': event,
        'upcomingevents': upcomingevents,
        'remaining_time_str': remaining_time_str,  
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
