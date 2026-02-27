from django.contrib import admin
from .models import WatchlistEntry

# -----------------------------------------------------------------------------
# Watchlist Entry Administration
# -----------------------------------------------------------------------------

@admin.register(WatchlistEntry)
class WatchlistEntryAdmin(admin.ModelAdmin):
    """
    Interface configuration for managing user watchlists in the Django Admin.
    Allows staff to monitor user engagement and filter entries by status.
    """
    # Columns shown in the main table list view
    list_display = ['id', 'user', 'media_id', 'status', 'added_at']
    
    # Filter sidebar for segregating entries by 'PLANNING', 'WATCHING', etc.
    list_filter = ['status']
    
    # Search functionality targeting usernames and specific AniList media IDs
    search_fields = ['user__username', 'media_id']