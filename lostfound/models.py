from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class LostandfoundItem(models.Model):
    
    category_choice = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found')
    ]

    category = models.CharField(max_length=5, choices=category_choice, blank=False)
    title = models.CharField(max_length=100, blank =False)
    product_description = models.TextField(blank =False)
    post_date = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(upload_to='lost_and_found_images/', blank =False)
    location = models.CharField(max_length=100, blank =False)
    # user = models.ForeignKey(User,on_delete=models.CASCADE)


    def __str__(self):
        return self.title