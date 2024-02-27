from django.urls import path
from . import views

app_name = "lostfound"
urlpatterns = [
    path('', views.index, name='home'),
]