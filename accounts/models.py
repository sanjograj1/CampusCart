from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/")

    def __str__(self):
        return f"Profile of {self.user.username}"


class Contact(models.Model):

    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    number = models.CharField(max_length=70, default="")


    def _str_(self):
        return self.name