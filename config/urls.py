from django.contrib import admin
from django.urls import include, path

from buses import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("buses.urls")),
]