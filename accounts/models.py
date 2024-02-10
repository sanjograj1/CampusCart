from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='images/', null=True, blank=True, default='images/default.png')

    def __str__(self):
        return self.username
