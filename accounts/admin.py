from django.contrib import admin
from .models import Profile, UserComment, Contact, UserRequest, UserSession, Report
from django.contrib.admin import ModelAdmin
from django.contrib.sessions.models import Session


class SessionAdmin(ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ['session_key', '_session_data', 'expire_date']


class CommentAdmin(ModelAdmin):
    list_display = ['comment', 'user', 'commented_by']


class ContactAdmin(ModelAdmin):
    list_display = ['name', 'message']


class UserRequestsAdmin(ModelAdmin):
    list_display = ['requested_by', 'item_name', 'item_category', 'requested_date']


# Register your models here.
admin.site.register(Profile)
admin.site.register(UserComment, CommentAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(UserSession)
admin.site.register(Report)
admin.site.register(UserRequest, UserRequestsAdmin)