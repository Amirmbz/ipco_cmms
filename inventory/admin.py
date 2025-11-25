from django.contrib import admin
from .models import Warehouse, PartCategory, Part, PartStock, PartTransaction


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'plant', 'location')
    list_filter = ('plant',)


@admin.register(PartCategory)
class PartCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'unit', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('code', 'name')


@admin.register(PartStock)
class PartStockAdmin(admin.ModelAdmin):
    list_display = ('part', 'warehouse', 'condition', 'quantity')
    list_filter = ('warehouse', 'condition')


@admin.register(PartTransaction)
class PartTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'part', 'quantity', 'warehouse_from', 'warehouse_to', 'created_at')
    list_filter = ('transaction_type', 'condition')