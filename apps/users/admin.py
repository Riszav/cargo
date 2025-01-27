from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'last_name', 'first_name', 'client_id')
    search_fields = ('username', 'last_name', 'first_name', 'client_id')
    list_filter = ('username', 'last_name', 'first_name', 'client_id')
    ordering = ('username', 'last_name', 'first_name', 'client_id')
    
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Персональная информация", 
            {"fields": 
                ("client_id", ("last_name", "first_name"), "email", "country", "phone_number", 
                ("tarif_usa", "tarif_usa_value"), ("tarif_turkey", "tarif_turkey_value"), ("tarif_china", "tarif_china_value"), ("tarif_japan", "tarif_japan_value"), 
                "inn", "status", "passport_number", "passport_date", "passport_place", "passport_image_1", "passport_image_2", "contract"
                )
            }
        ),
        ("Права",{"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

