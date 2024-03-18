from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("profile/<username>", views.profile_view, name="profile_view"),
    path("logout/", views.user_logout, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("profile/listing/", views.user_listing, name="user-listing"),
    path(
        "profile/listing/edit/<str:model>/<int:id>/",
        views.toggle_sold_status,
        name="toggle-sold-status",
    ),
    path("profile/rating/<username>", views.user_rating, name="user-rating"),
    path('notifications/', views.notifications_view, name='notifications'),
    path('contactus/', views.contactus, name='contactus'),
    path('login-history/', views.login_history, name='login-history'),
    path('change-theme/', views.change_theme, name='change-theme'),
    path("change-password/", views.change_password, name="change-password")
]