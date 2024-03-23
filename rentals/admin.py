from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Rental, RentalViews


class RentalAdmin(ModelAdmin):
    list_display = ['property_name','address','seller','is_sold']


class RentalViewsAdmin(ModelAdmin):
    list_display = ['user', 'rental', 'viewed_at']

# Register your models here.
admin.site.register(Rental, RentalAdmin)
admin.site.register(RentalViews, RentalViewsAdmin)
