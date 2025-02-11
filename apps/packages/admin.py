from django.contrib import admin
from . import models
from config.base_admin import BaseSoloAdmin


@admin.register(models.WarehouseData)
class WarehouseDataAdmin(BaseSoloAdmin):
    fieldsets = [
        ('США', {
            'fields': ['usa_address_1', 'usa_address_2', 'usa_city', 'usa_state', 'usa_zip_code', 'usa_phone'],
        }), 
        ('Турция', {
            'fields': ['turkey_city', 'turkey_rayon', 'turkey_quarter', 'turkey_address', 'turkey_post_code', 'turkey_phone'],
        }),
        ('Китай', {
            'fields': ['china_address', 'china_phone', 'china_region', 'china_detail_address', 'china_post_code'],
        }),
        ('Япония', {
            'fields': ['japan_city', 'japan_address', 'japan_post_code', 'japan_phone']
        })
    ]
    

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    

@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


class PackageDetailInline(admin.TabularInline):
    model = models.PackageDetail
    extra = 1
    
class PackageImageInline(admin.TabularInline):
    model = models.PackageImage
    extra = 1

class PackageWeightInline(admin.TabularInline):
    model = models.PackageWeight
    extra = 1


@admin.register(models.Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'recipient', 'status', 'warehouse', 'created_at']
    list_display_links = ['id', 'client', 'recipient', 'warehouse', 'created_at']
    list_editable = ['status',]
    list_filter = ['created_at']
    search_fields = ['client', 'recipient']
    inlines = [PackageDetailInline, PackageImageInline, PackageWeightInline]
    
    
@admin.register(models.Scan)
class ScanAdmin(admin.ModelAdmin):
    list_display = ['id', 'tracking_number', 'tracking_number_2', 'manager', 'type', 'location', 'updated_at', 'created_at']
    list_display_links = ['id', 'tracking_number', 'tracking_number_2', 'manager', 'type', 'location', 'updated_at', 'created_at']
    list_filter = ['updated_at', 'created_at', 'type']
    search_fields = ['tracking_number', 'tracking_number_2']
    

@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


class AWBFileInline(admin.TabularInline):
    model = models.AWBFile
    extra = 1


@admin.register(models.AWB)
class AWBAdmin(admin.ModelAdmin):
    list_display = ['id', 'number']
    search_fields = ['number']
    inlines = [AWBFileInline]

