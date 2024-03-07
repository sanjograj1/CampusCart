from django.contrib import admin
from .models import Profile,UserComment, Contact

# Register your models here.
admin.site.register(Profile)
admin.site.register(UserComment)
admin.site.register(Contact)
