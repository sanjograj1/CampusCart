from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import FreeStuffItem, FreeItemViews


class FreeStuffItemAdmin(ModelAdmin):
    list_display = ['title', 'condition', 'seller', 'is_sold']


class FreeViewsAdmin(ModelAdmin):
    list_display = ['user', 'free', 'viewed_at']


# Register your models here.
admin.site.register(FreeStuffItem, FreeStuffItemAdmin)
admin.site.register(FreeItemViews, FreeViewsAdmin)
