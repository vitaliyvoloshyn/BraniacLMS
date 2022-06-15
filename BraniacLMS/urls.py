from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView


urlpatterns = [
    path("admin/", admin.site.urls, name='admin'),
    path("", RedirectView.as_view(url="mainapp/")),
    path("mainapp/", include("mainapp.urls")),
    path("authapp/", include("authapp.urls")),
    path("social_auth/", include("social_django.urls", namespace="social")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

