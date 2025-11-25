from django.contrib import admin
from .models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'address')
    search_fields = ('code', 'name')