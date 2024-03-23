from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Product, ProductViews


class ProductAdmin(ModelAdmin):
    list_display = ['title', 'price', 'user', 'is_sold']


class ProductViewsAdmin(ModelAdmin):
    list_display = ['user', 'product', 'viewed_at']


# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductViews, ProductViewsAdmin)
