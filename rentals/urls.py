from django.urls import path
from . import views

app_name='rentals'
urlpatterns=[
    path('',views.rental_home,name='home'),
    path('property-detail/<int:rentid>',views.property_detail,name='property-detail'),
    path('edit-property/<int:rentid>',views.edit_property,name='edit-property'),
    path('upload-property',views.upload_property,name='upload-property')
]