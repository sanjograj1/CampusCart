from django.contrib import admin
from .models import Profile,UserComment, Contact, UserSession,Report
from django.contrib.admin import ModelAdmin
from django.contrib.sessions.models import Session


class SessionAdmin(ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ['session_key', '_session_data', 'expire_date']


# Register your models here.
admin.site.register(Profile)
admin.site.register(UserComment)
admin.site.register(Contact)
admin.site.register(Session, SessionAdmin)
admin.site.register(UserSession)
admin.site.register(Report)
