from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class FreeStuffItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_image = models.ImageField(upload_to='freestuff/', default='freestuff/default.png')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
