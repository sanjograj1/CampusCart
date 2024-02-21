from django.urls import path
from . import views

app_name = "freestuff"
urlpatterns = [
    path('', views.index, name='home'),
]