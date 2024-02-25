from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to="profile_images/",default='profile_images/default.png')

    def __str__(self):
        return f"Profile of {self.user.username}"

class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="commented_by")
    comment = models.TextField()
    commented_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Rating for {self.user.username}'
