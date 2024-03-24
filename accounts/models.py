from django.db import models

from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    user_class = models.CharField("Class", max_length=50, blank=True, null=True)
    course = models.CharField(max_length=50, blank=True, null=True)
    profile_image = models.ImageField(
        upload_to="profile_images/", default="profile_images/default.png"
    )

    def __str__(self):
        return f"Profile of {self.user.username}"


class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commented_by")
    comment = models.TextField()
    commented_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Rating for {self.user.username}'


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=70)
    number = models.CharField(
        "Phone Number", max_length=15, help_text="Enter your number  "
    )
    message = models.TextField()

    def _str_(self):
        return self.name


class UserSession(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    session_key = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"


# Report Models for User
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reported_by"
    )
    report = models.TextField()
    reported_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.user.username}"


class UserRequest(models.Model):
    ITEM_CATEGORY = [
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Shoes', 'Shoes'),
        ('Furniture', 'Furniture'),
        ('Book', 'Book'),
        ('Rental', 'Rental'),
    ]
    item_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    item_category = models.CharField(choices=ITEM_CATEGORY, max_length=50)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requested_by.get_full_name()} requested {self.item_name} under {self.item_category} Category"