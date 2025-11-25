from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'plant', 'parent', 'department')
    list_filter = ('plant', 'department')
    search_fields = ('code', 'name')