from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("auth.urls")),
    path("", include("cryptos.urls")),
    path("admin/", admin.site.urls),
]
