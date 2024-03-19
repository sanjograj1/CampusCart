from django.db import models


from django.contrib.auth.models import User

CATEGORY_LIST = [
    ("Electronics", "Electronics"),
    ("Clothing", "Clothing"),
    ("Shoes", "Shoes"),
    ("Furniture", "Furniture"),
    ("Others", "Others"),
]


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, choices=CATEGORY_LIST)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="product_images/")
    interested_users = models.ManyToManyField(User, related_name="interested_products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_sold = models.BooleanField(default=False)

    # check product is interested by user or not
    def is_interested(self, user):
        return self.interested_users.filter(id=user.id).exists()

    def __str__(self):
        return self.title
