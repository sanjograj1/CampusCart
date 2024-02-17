from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name="profile"),
]
