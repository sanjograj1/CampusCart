from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Rental(models.Model):
    CHOICE_FIELD = [
        ('Yes', 'Yes'),
        ('No', 'No')
    ]
    property_name = models.CharField(max_length=50)
    property_image = models.ImageField(
        upload_to="upload_property/"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100, default="Windsor")
    zip_code = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    is_sold = models.BooleanField(default=False)
    bedrooms = models.PositiveIntegerField(default=1, blank=True)
    bathrooms = models.PositiveIntegerField(default=1, blank=True)
    furnished = models.CharField(max_length=5, choices=CHOICE_FIELD, default='No', blank=True)
    agreement = models.PositiveIntegerField(default=1, blank=True)
    appliances = models.CharField(max_length=5, choices=CHOICE_FIELD, default='Yes', blank=True)
    parking = models.CharField(max_length=5, choices=CHOICE_FIELD, default='No', blank=True)

    def __str__(self):
        return self.property_name
