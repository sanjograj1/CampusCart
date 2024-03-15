from django.urls import path
from . import views

app_name='rentals'
urlpatterns=[
    path('',views.rental_home,name='home'),
    path('upload-property',views.upload_property,name='upload-property')
]