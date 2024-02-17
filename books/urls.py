from django.urls import path
from . import views

app_name = "books"
urlpatterns = [
    path('', views.bookhome, name='home'),
    path('upload', views.upload_book, name='upload-book'),
]
