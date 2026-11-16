from django.urls import path

from . import views

urlpatterns = [
    path("", views.search, name="search"),
    path("book/", views.book, name="book"),
    path("signup/", views.signup, name="signup"),
]