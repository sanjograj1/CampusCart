from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    EVENT_CATEGORY = [
        ("Workshop", "Workshop"),
        ("Concert", "Concert"),
        ("Festival", "Festival"),
        ("Exhibition", "Exhibition"),
        ("Seminar", "Seminar"),
        ("Sports", "Sports"),
        ("Entertainment", "Entertainment"),
        ("Other", "Other"),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=EVENT_CATEGORY, default="Other")
    date_and_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField(default=0)
    attendees_count = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to="event/", default="event/events.jpg", blank=True
    )
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def seats_remaining(self):
        return max(0, self.total_seats - self.attendees_count)
