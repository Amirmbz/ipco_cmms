from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'work_order', 'created_at', 'read')
    list_filter = ('type', 'read')