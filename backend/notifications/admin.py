from django.contrib import admin
from .models import Notifications

@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('user_id__username', 'message')