from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("verification/", include("verify_email.urls")),
    path("", include("accounts.urls", namespace="accounts")),
    path("", include("products.urls", namespace="products")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
