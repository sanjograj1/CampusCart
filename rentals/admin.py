from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Rental


class RentalAdmin(ModelAdmin):
    list_display = ['property_name','address','seller','is_sold']


# Register your models here.
admin.site.register(Rental, RentalAdmin)
