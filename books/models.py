from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Book(models.Model):
    BOOKS_CATEGORY = [
        ("Fiction", "Fiction"),
        ("Non-Fiction", "Non-Fiction"),
        ("Academic", "Academic"),
        ("Children", "Children"),
        ("Art & Photography", "Art & Photography"),
        ("Cookbooks", "Cookbooks"),
        ("Travel", "Travel"),
        ("Health & Wellness", "Health & Wellness"),
        ("Religion & Spirituality", "Religion & Spirituality"),
        ("Hobbies & Crafts", "Hobbies & Crafts"),
        ("Sports & Recreation", "Sports & Recreation"),
        ("Science Fiction & Fantasy", "Science Fiction & Fantasy"),
        ("Horror", "Horror"),
        ("Poetry", "Poetry"),
        ("Drama", "Drama"),
        ("Others", "Others"),
    ]
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    pages = models.PositiveIntegerField()
    language = models.CharField(max_length=50, default="English")
    category = models.CharField(
        max_length=50, choices=BOOKS_CATEGORY, default="Others", blank=True
    )
    book_cover = models.ImageField(
        upload_to="upload_book/", default="upload_book/book-cover.png", blank=True
    )
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.title
