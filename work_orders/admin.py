from django.contrib import admin
from .models import (
    WorkOrderGroup,
    WorkOrder,
    WorkOrderFailure,
    WorkOrderAction,
    WorkOrderPartUsage,
    WorkOrderAttachment,
    WorkOrderComment,
)


@admin.register(WorkOrderGroup)
class WorkOrderGroupAdmin(admin.ModelAdmin):
    list_display = ('code', 'plant', 'created_at')


class WorkOrderFailureInline(admin.TabularInline):
    model = WorkOrderFailure
    extra = 0


class WorkOrderActionInline(admin.TabularInline):
    model = WorkOrderAction
    extra = 0


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ('code', 'plant', 'department', 'status', 'type', 'priority')
    list_filter = ('plant', 'department', 'status', 'type', 'priority')
    search_fields = ('code', 'title')
    inlines = [WorkOrderFailureInline, WorkOrderActionInline]


admin.site.register(WorkOrderFailure)
admin.site.register(WorkOrderAction)
admin.site.register(WorkOrderPartUsage)
admin.site.register(WorkOrderAttachment)
admin.site.register(WorkOrderComment)