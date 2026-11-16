from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import Booking, Bus, Route


@admin.register(Route)
class RouteAdmin(ModelAdmin):
    list_display = ("source", "destination")
    search_fields = ("source", "destination")


@admin.register(Bus)
class BusAdmin(ModelAdmin):
    list_display = ("operator", "route", "bus_type", "departure_time", "price", "total_seats")
    list_filter = ("bus_type", "route")
    search_fields = ("operator",)
    ordering = ("route", "departure_time")


@admin.register(Booking)
class BookingAdmin(ModelAdmin):
    list_display = ("user", "bus", "travel_date", "seat_number", "created_at")
    list_filter = ("travel_date", "bus")
    search_fields = ("user__username", "bus__operator")
    date_hierarchy = "travel_date"


# Style the built-in Users and Groups pages with the Unfold theme too
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass