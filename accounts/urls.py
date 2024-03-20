from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)


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
     path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
        ),
        name="password-reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    path("profile/rating/<username>", views.user_rating, name="user-rating"),
    path('notifications/', views.notifications_view, name='notifications'),
    path('contactus/', views.contactus, name='contactus'),
    path('login-history/', views.login_history, name='login-history'),
    path('change-theme/', views.change_theme, name='change-theme'),
    path("change-password/", views.change_password, name="change-password")
]