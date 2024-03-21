from django.contrib import admin
from django.contrib.admin import ModelAdmin
 
from .models import Book
 
 
class BookAdmin(ModelAdmin):
    list_display = ['title', 'author','category', 'seller', 'is_sold']
 
 
# Register your models here.
admin.site.register(Book, BookAdmin)