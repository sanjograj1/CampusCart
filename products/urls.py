from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path("", views.home, name="home"),
    path("sell/", views.create_product, name="sell"),
]
