from django.urls import path
from . import views

app_name = "events"
urlpatterns = [
    path('', views.eventshome, name='event-home'),
    path('detail/', views.eventdetail, name='event-detail'),

]
