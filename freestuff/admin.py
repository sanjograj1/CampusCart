from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import FreeStuffItem
 
 
class FreeStuffItemAdmin(ModelAdmin):
    list_display = ['title', 'condition', 'seller','is_sold']
 
 
# Register your models here.
admin.site.register(FreeStuffItem, FreeStuffItemAdmin)