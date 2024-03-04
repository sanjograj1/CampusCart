from django.urls import path
from . import views

app_name = "products"
urlpatterns = [
    path("", views.home, name="home"),
    path("sell/", views.create_product, name="sell"),
    path("detail-product/<int:pk>/", views.detail_product, name="detail_product"),
    path('edit/<int:productid>', views.edit_product, name='edit-product'),
    path(
        "interested-product/<int:pk>/",
        views.interested_product,
        name="interested_product",
    ),
]
