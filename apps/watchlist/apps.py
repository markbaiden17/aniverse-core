from django.apps import AppConfig

# -----------------------------------------------------------------------------
# Watchlist App Configuration
# -----------------------------------------------------------------------------

class WatchlistConfig(AppConfig):
    """
    Configuration class for the watchlist application.
    This app manages personal user lists, tracking anime titles that 
    users are currently watching, planning to watch, or have completed.
    """
    # Standardizes the primary key type for the watchlist tables
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The full Python path used by Django's internal registry
    name = 'apps.watchlist'