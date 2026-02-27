from django.contrib import admin
from .models import Review

# -----------------------------------------------------------------------------
# Review Administration Configuration
# -----------------------------------------------------------------------------

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Customizes the Django Admin interface for the Review model.
    Provides tools for moderating user feedback and tracking ratings.
    """
    # Columns to display in the list view for quick oversight
    list_display = ['id', 'user', 'media_id', 'rating', 'created_at']
    
    # Sidebar filters for narrowing down reviews by specific criteria
    list_filter = ['rating', 'created_at']
    
    # Enable keyword searches across usernames, anime IDs, and review text
    search_fields = ['user__username', 'media_id', 'comment']
    
    # Default display order (most recent reviews first)
    ordering = ['-created_at']