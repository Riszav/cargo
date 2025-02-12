from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models


@admin.register(models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name', 'is_active')
    list_filter = ('name', 'is_active')
    ordering = ('name', 'is_active')


class RecipientInline(admin.StackedInline):
    model = models.Recipient
    extra = 1


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'is_admin', 'is_manager', 'email', 'phone_number', 'last_name', 'first_name', 'client_id')
    list_display_links = ('id', 'is_admin', 'is_manager', 'email', 'phone_number', 'last_name', 'first_name', 'client_id')
    search_fields = ('email', 'phone_number', 'last_name', 'first_name', 'client_id')
    list_filter = ('email', 'phone_number', 'last_name', 'first_name', 'client_id')
    ordering = ('-date_joined',)
    inlines = [RecipientInline]
    readonly_fields = ('client_id',)
    # add_form = UserCreationForm
    
    fieldsets = (
        (None, {"fields": ("email", 'phone_number', "password")}),
        (
            "Персональная информация", 
            {"fields": 
                ("client_id", ("last_name", "first_name"), "country", 
                ("tarif_usa", "tarif_usa_value"), 'tarif_usa_weight', ("tarif_turkey", "tarif_turkey_value"), 'tarif_turkey_weight', 
                ("tarif_china", "tarif_china_value"), 'tarif_china_weight', ("tarif_japan", "tarif_japan_value"), 'tarif_japan_weight', 
                'is_admin', 'is_manager'
                )
            }
        ),
        ("Права",{"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Важные даты", {"fields": ("last_login", "date_joined")}),
    )

