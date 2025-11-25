from django.contrib import admin
from .models import AssetCategory, Asset, AssetAttachment, AssetSparePartLink


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class AssetAttachmentInline(admin.TabularInline):
    model = AssetAttachment
    extra = 0


class AssetSparePartInline(admin.TabularInline):
    model = AssetSparePartLink
    extra = 0


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'plant', 'location', 'status', 'pm_schedule_type')
    list_filter = ('plant', 'status', 'pm_schedule_type', 'category')
    search_fields = ('code', 'name')
    inlines = [AssetAttachmentInline, AssetSparePartInline]


@admin.register(AssetAttachment)
class AssetAttachmentAdmin(admin.ModelAdmin):
    list_display = ('asset', 'file', 'description')


@admin.register(AssetSparePartLink)
class AssetSparePartLinkAdmin(admin.ModelAdmin):
    list_display = ('asset', 'part', 'notes')