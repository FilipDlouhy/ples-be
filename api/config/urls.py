from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.user.urls")),
    path("api/", include("apps.reservations.urls")),
    path("api/", include("apps.salons.urls")),
    path("api/", include("apps.content.urls")),
    path("api/", include("apps.site_config.urls")),
]
