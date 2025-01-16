from django.contrib import admin
from config.base_admin import BaseSoloAdmin, BaseImageAdmin
from . import models


@admin.register(models.Banner)
class BannerAdmin(BaseImageAdmin):
    list_display = ['title', 'view_min']
    list_display_links = ['title', 'view_min']
    fields = ['title', 'image', 'view_max']
    readonly_fields = ['view_min', 'view_max']
    search_fields = ['title']
    list_filter = ['title']


@admin.register(models.AboutUs)
class AboutUsAdmin(BaseImageAdmin):
    list_display = ['title', 'view_min']
    list_display_links = ['title', 'view_min']
    fields = ['title', 'description', 'image', 'view_max']
    readonly_fields = ['view_min', 'view_max']
    search_fields = ['title']
    list_filter = ['title']


@admin.register(models.AboutUsPage)
class AboutUsPageAdmin(BaseSoloAdmin, BaseImageAdmin):
    list_display = ['text', 'view_min1', 'view_min2']
    list_display_links = ['text', 'view_min1', 'view_min2']
    fields = ['text', 'image1', 'view_max1', 'image2', 'view_max2']
    readonly_fields = ['view_min1', 'view_min2', 'view_max1', 'view_max2']
    search_fields = ['text']
    list_filter = ['text']


@admin.register(models.OurServices)
class OurServicesAdmin(BaseImageAdmin):
    list_display = ['title', 'view_min']
    list_display_links = ['title', 'view_min']
    fields = ['title', 'description', 'image', 'view_max']
    readonly_fields = ['view_min', 'view_max']
    search_fields = ['title']
    list_filter = ['title']
    
    
@admin.register(models.ApplicationSettings)
class ApplicationSettingsAdmin(BaseSoloAdmin):
    list_display = ['title']
    list_display_links = ['title']
    search_fields = ['title']
    list_filter = ['title']
    

@admin.register(models.Application)
class ApplicationAdmin(BaseImageAdmin):
    list_display = ['name', 'phone', 'email', 'message']
    list_display_links = ['name', 'phone', 'email', 'message']
    search_fields = ['name', 'phone', 'email', 'message']
    list_filter = ['name', 'phone', 'email', 'message']
    

@admin.register(models.FAQ)
class FAQAdmin(BaseImageAdmin):
    list_display = ['question', 'answer']
    list_display_links = ['question', 'answer']
    search_fields = ['question', 'answer']
    list_filter = ['question', 'answer']
    

@admin.register(models.Gallery)
class GalleryAdmin(BaseImageAdmin):
    list_display = ['view_min']
    list_display_links = ['view_min']
    fields = ['image', 'view_max']
    readonly_fields = ['view_min', 'view_max']
    search_fields = ['image']
    list_filter = ['image']
    
    
@admin.register(models.HowItWorks)
class HowItWorksAdmin(BaseImageAdmin):
    list_display = ['title', 'view_min']
    list_display_links = ['title', 'view_min']
    fields = ['title', 'description', 'image', 'view_max']
    readonly_fields = ['view_min', 'view_max']
    search_fields = ['title']
    list_filter = ['title']
    

@admin.register(models.PriceAndPayment)
class PriceAndPaymentAdmin(BaseImageAdmin):
    list_display = ['weight', 'type_of_service', 'price_usa', 'price_turkey', 'price_china_air', 'price_china_car', 'commission']
    list_display_links = ['weight', 'type_of_service', 'price_usa', 'price_turkey', 'price_china_air', 'price_china_car', 'commission']
    search_fields = ['weight', 'type_of_service', 'price_usa', 'price_turkey', 'price_china_air', 'price_china_car', 'commission']
    list_filter = ['weight', 'type_of_service', 'price_usa', 'price_turkey', 'price_china_air', 'price_china_car', 'commission']
    
    
@admin.register(models.PaymentData)
class PaymentDataAdmin(BaseSoloAdmin):
    list_display = ['subtitle', 'description', 'description_weight', 'text_weight', 'description_payment']
    list_display_links = ['subtitle', 'description', 'description_weight', 'text_weight', 'description_payment']
    search_fields = ['subtitle', 'description', 'description_weight', 'text_weight', 'description_payment']
    list_filter = ['subtitle', 'description', 'description_weight', 'text_weight', 'description_payment']


@admin.register(models.News)
class NewsAdmin(BaseImageAdmin):
    list_display = ['title',]
    list_display_links = ['title',]
    search_fields = ['title', 'description']
    list_filter = ['title',]


@admin.register(models.PVZ)
class PVZAdmin(BaseImageAdmin):
    list_display = ['title', 'location', 'phone_number', 'working_hours']
    list_display_links = ['title', 'location', 'phone_number', 'working_hours']
    search_fields = ['title', 'location', 'phone_number', 'working_hours']
    list_filter = ['title', 'location', 'phone_number', 'working_hours']

