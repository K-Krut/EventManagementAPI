from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'first_name', 'last_name', 'email', 'email_notifications', 'registration_date', 'is_superuser', 'is_staff',
        'is_active'
    ]
    list_filter = ['email_notifications', 'registration_date', 'is_superuser', 'is_staff', 'is_active']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['registration_date', 'first_name', 'last_name']
    show_facets = admin.ShowFacets.ALWAYS
