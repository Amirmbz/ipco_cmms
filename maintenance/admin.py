from django.contrib import admin
from .models import (
    PMTemplate,
    PMSchedule,
    ChecklistTemplate,
    ChecklistItemTemplate,
    ChecklistExecution,
    ChecklistItemExecution,
)


class ChecklistItemInline(admin.TabularInline):
    model = ChecklistItemTemplate
    extra = 0


@admin.register(PMTemplate)
class PMTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'plant', 'frequency_type', 'interval_days', 'interval_hours', 'active')
    list_filter = ('plant', 'frequency_type', 'active')


@admin.register(PMSchedule)
class PMScheduleAdmin(admin.ModelAdmin):
    list_display = ('template', 'asset', 'next_due_date', 'active')
    list_filter = ('active',)


@admin.register(ChecklistTemplate)
class ChecklistTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'plant')
    inlines = [ChecklistItemInline]


admin.site.register(ChecklistItemTemplate)
admin.site.register(ChecklistExecution)
admin.site.register(ChecklistItemExecution)