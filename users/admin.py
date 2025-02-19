from django.contrib import admin
from django.utils import formats

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 'last_name', 'email', 'email_notifications', 'formatted_registration_date', 'is_superuser',
        'is_staff', 'is_active'
    ]
    list_filter = ['email_notifications', 'registration_date', 'is_superuser', 'is_staff', 'is_active']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['registration_date', 'first_name', 'last_name']
    show_facets = admin.ShowFacets.ALWAYS

    def formatted_registration_date(self, obj):
        return formats.date_format(obj.registration_date, "Y-m-d")

    formatted_registration_date.short_description = 'Registration Date'
