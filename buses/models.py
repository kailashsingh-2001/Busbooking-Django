from django.conf import settings
from django.db import models


class Route(models.Model):
    source = models.CharField(max_length=80)
    destination = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.source} to {self.destination}"


class Bus(models.Model):
    BUS_TYPES = [
        ("AC_SLEEPER", "AC sleeper"),
        ("AC_SEATER", "AC seater"),
        ("NONAC_SEATER", "Non-AC seater"),
    ]
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="buses")
    operator = models.CharField(max_length=100)
    bus_type = models.CharField(max_length=20, choices=BUS_TYPES)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    total_seats = models.PositiveIntegerField(default=20)

    @property
    def duration_text(self):
        h, m = divmod(self.duration_minutes, 60)
        return f"{h}h {m:02d}m"

    def __str__(self):
        return f"{self.operator} ({self.route})"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    travel_date = models.DateField()
    seat_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # The database itself blocks double-booking of the same seat.
        constraints = [
            models.UniqueConstraint(
                fields=["bus", "travel_date", "seat_number"], name="unique_seat_per_bus_per_day"
            )
        ]