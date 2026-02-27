from django.apps import AppConfig

# -----------------------------------------------------------------------------
# Reviews App Configuration
# -----------------------------------------------------------------------------

class ReviewsConfig(AppConfig):
    """
    Configuration class for the reviews application.
    Manages user-generated content, ratings, and media feedback.
    """
    # Standardizes the primary key type for all review-related tables
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Internal path used by Django to locate the application
    name = 'apps.reviews'