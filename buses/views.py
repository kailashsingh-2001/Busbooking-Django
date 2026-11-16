from datetime import date
from django.contrib.auth import login
from django.contrib.auth import logout
from .forms import SignUpForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.dateparse import parse_date

from .models import Booking, Bus

TYPE_FILTERS = {"AC": "AC_", "Sleeper": "SLEEPER", "Seater": "SEATER"}


def search(request):
    source = request.GET.get("source", "Jaipur")
    destination = request.GET.get("destination", "Delhi")
    travel_date = parse_date(request.GET.get("date", "") or "") or date.today()
    bus_filter = request.GET.get("type")

    buses = Bus.objects.filter(
        route__source__iexact=source, route__destination__iexact=destination
    ).select_related("route")

    if bus_filter in TYPE_FILTERS:
        buses = buses.filter(bus_type__contains=TYPE_FILTERS[bus_filter])

    buses = buses.annotate(
        booked_count=Count("booking", filter=Q(booking__travel_date=travel_date))
    ).annotate(seats_left=F("total_seats") - F("booked_count"))

    selected_bus = None
    seat_rows = []
    bus_id = request.GET.get("bus")
    if bus_id:
        selected_bus = get_object_or_404(buses, pk=bus_id)
        booked = set(
            Booking.objects.filter(bus=selected_bus, travel_date=travel_date)
            .values_list("seat_number", flat=True)
        )
        seats = [
            {"number": n, "booked": n in booked}
            for n in range(1, selected_bus.total_seats + 1)
        ]
        seat_rows = [seats[i:i + 4] for i in range(0, len(seats), 4)]

    return render(request, "buses/search.html", {
        "buses": buses,
        "source": source,
        "destination": destination,
        "travel_date": travel_date,
        "selected_bus": selected_bus,
        "seat_rows": seat_rows,
    })


@login_required
def book(request):
    if request.method != "POST":
        return redirect("search")

    bus = get_object_or_404(Bus, pk=request.POST.get("bus"))
    travel_date = parse_date(request.POST.get("date", ""))
    seats = [int(s) for s in request.POST.get("seats", "").split(",") if s.isdigit()]

    if not travel_date or not seats:
        messages.error(request, "Choose a date and at least one seat.")
        return redirect("search")

    try:
        with transaction.atomic():
            for seat in seats:
                Booking.objects.create(
                    user=request.user, bus=bus, travel_date=travel_date, seat_number=seat
                )
    except IntegrityError:
        messages.error(request, "One of those seats was just booked. Pick another seat.")
        return redirect("search")

    messages.success(request, f"Booked seats {', '.join(map(str, seats))}.")
    return redirect("search")


def signup(request):
    # if request.user.is_authenticated:
    #     return redirect("search")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created. Welcome to BusBook!")
            return redirect("search")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})



def logout_view(request):
    logout(request)
    return redirect("search")