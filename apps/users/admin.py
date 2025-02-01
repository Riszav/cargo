from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name', 'is_active')
    list_filter = ('name', 'is_active')
    ordering = ('name', 'is_active')


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ('is_admin', 'email', 'phone_number', 'last_name', 'first_name', 'client_id')
    list_display_links = ('is_admin', 'email', 'phone_number', 'last_name', 'first_name', 'client_id')
    search_fields = ('email', 'phone_number', 'last_name', 'first_name', 'client_id')
    list_filter = ('email', 'phone_number', 'last_name', 'first_name', 'client_id')
    ordering = ('-date_joined',)
    # add_form = UserCreationForm
    
    fieldsets = (
        (None, {"fields": ("email", 'phone_number', "password")}),
        (
            "Персональная информация", 
            {"fields": 
                ("client_id", ("last_name", "first_name"), "country", 
                ("tarif_usa", "tarif_usa_value"), 'tarif_usa_weight', ("tarif_turkey", "tarif_turkey_value"), 'tarif_turkey_weight', 
                ("tarif_china", "tarif_china_value"), 'tarif_china_weight', ("tarif_japan", "tarif_japan_value"), 'tarif_japan_weight', 
                "inn", "status", "passport_number", "passport_date", "passport_place", "passport_image_1", "passport_image_2", "contract", 'is_admin'
                )
            }
        ),
        ("Права",{"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

