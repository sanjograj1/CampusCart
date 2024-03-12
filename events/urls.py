from django.urls import path
from . import views

app_name = "events"
urlpatterns = [
    path('', views.eventshome, name='event-home'),
    path('event-detail/<int:event_id>', views.eventdetail, name='event-detail'),
    path('upload-event/', views.uploadevent, name='upload-event'),
]
