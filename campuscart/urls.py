import notifications.urls
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)



urlpatterns = [
    path("admin/", admin.site.urls),
    path("verification/", include("verify_email.urls")),
    path("", include("accounts.urls", namespace="accounts")),
    path("product/", include("products.urls", namespace="products")),
    path('books/', include('books.urls',namespace="books")),
    path('events/', include('events.urls',namespace="events")),
    path('free/', include('freestuff.urls',namespace="freestuff")),
    path('lostandfound/', include('lostfound.urls',namespace="lostfound")),
    path('rentals/',include('rentals.urls',namespace="rentals")),
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


    path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
