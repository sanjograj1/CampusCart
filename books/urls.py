from django.urls import path
from . import views

app_name = "books"
urlpatterns = [
    path('', views.furniture, name='home'),
]
