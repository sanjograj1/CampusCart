import notifications.urls
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("verification/", include("verify_email.urls")),
    path("", include("accounts.urls", namespace="accounts")),
    path("product/", include("products.urls", namespace="products")),
    path('books/', include('books.urls',namespace="books")),
    path('events/', include('events.urls',namespace="events")),
    path('free/', include('freestuff.urls',namespace="freestuff")),
    path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
