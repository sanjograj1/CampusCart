from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Book, BookViews


class BookAdmin(ModelAdmin):
    list_display = ['title', 'author', 'category', 'seller', 'is_sold']


class BookViewsAdmin(ModelAdmin):
    list_display = ['user', 'book','viewed_at']

# Register your models here.


admin.site.register(Book, BookAdmin)
admin.site.register(BookViews, BookViewsAdmin)
