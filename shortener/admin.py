from django.contrib import admin
from .models import URL


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    """
    Admin configuration for the URL model.
    Customizes how URL records appear and
    behave inside the Django Admin panel.
    """

    # Columns shown in the list view
    list_display = [
        'short_code',
        'original_url',
        'click_count',
        'created_at',
    ]

    # Clickable link column to open the record
    list_display_links = ['short_code']

    # Right sidebar filters
    list_filter = ['created_at']

    # Search bar — searches these fields
    search_fields = ['short_code', 'original_url']

    # Fields that cannot be edited in admin
    readonly_fields = ['short_code', 'created_at', 'click_count']

    # Default sort — newest first
    ordering = ['-created_at']

    # How many records per page
    list_per_page = 20

    # Field layout inside the detail/edit view
    fieldsets = (
        ('URL Information', {
            'fields': ('original_url', 'short_code')
        }),
        ('Statistics', {
            'fields': ('click_count', 'created_at')
        }),
    )