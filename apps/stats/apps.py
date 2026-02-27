from django.apps import AppConfig

# -----------------------------------------------------------------------------
# Stats App Configuration
# -----------------------------------------------------------------------------

class StatsConfig(AppConfig):
    """
    Configuration class for the stats application.
    This app handles data aggregation, rating distributions, and 
    analytical insights for the AniVerse platform.
    """
    # Sets the default primary key type for all models in this app
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The full Python path used by Django's registry to identify the app
    name = 'apps.stats'