# Generated by Django 5.0.1 on 2024-03-05 01:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("location", models.CharField(max_length=100)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("Workshop", "Workshop"),
                            ("Concert", "Concert"),
                            ("Festival", "Festival"),
                            ("Exhibition", "Exhibition"),
                            ("Seminar", "Seminar"),
                            ("Sports", "Sports"),
                            ("Entertainment", "Entertainment"),
                            ("Other", "Other"),
                        ],
                        default="Other",
                        max_length=50,
                    ),
                ),
                ("date_and_time", models.DateTimeField()),
                ("total_seats", models.PositiveIntegerField(default=0)),
                ("attendees_count", models.PositiveIntegerField(default=0)),
                (
                    "image",
                    models.ImageField(
                        blank=True, default="event/events.jpg", upload_to="event/"
                    ),
                ),
                (
                    "organizer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]