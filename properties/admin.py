"""
Admin configuration for properties app.
"""
from django.contrib import admin
from .models import Property


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """Admin interface for Property model."""
    list_display = ('title', 'location', 'price', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('title', 'description', 'location')
    readonly_fields = ('created_at',)
