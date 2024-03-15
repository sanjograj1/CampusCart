from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Rental(models.Model):
    property_name=models.CharField(max_length=50)
    property_image=models.ImageField(upload_to='upload_property/',default='upload_property/property_sample.jpg')
    price=models.DecimalField(max_digits=10,decimal_places=2)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    description=models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    seller=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.property_name
