from django.urls import path
from . import views

app_name = "lostfound"
urlpatterns = [
    path('', views.index, name='home'),
    path('post_detail/<int:post_id>/', views.laf_detail, name='detail'),
    path('upload/', views.post, name='upload'),
    path('edit/<int:postid>', views.editpost, name='edit-post'),       
]