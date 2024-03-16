from django.db import models

# Create your models here.
class LostandfoundItem(models.Model):
    
    category_choice = [
        ('LOST', 'Lost'),
        ('FOUND', 'Found')
    ]

    category = models.CharField(max_length=5, choices=category_choice)
    title = models.CharField(max_length=100)
    product_description = models.TextField()
    post_date = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(upload_to='lost_and_found_images/')
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.title