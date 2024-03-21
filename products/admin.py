from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Product


class ProductAdmin(ModelAdmin):
    list_display = ['title', 'price', 'user', 'is_sold']


admin.site.register(Product, ProductAdmin)