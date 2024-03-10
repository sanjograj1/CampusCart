from django.urls import path
from . import views

app_name = "freestuff"
urlpatterns = [
    path('', views.index, name='home'),
    path('upload', views.upload_item, name='upload-item'),
    path('item-detail/<int:itemid>', views.item_detail, name='item-detail'),
    path('edit/<int:itemid>', views.edit_item, name='edit-item'),
]