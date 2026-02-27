from django.apps import AppConfig

# -----------------------------------------------------------------------------
# Authentication App Configuration
# -----------------------------------------------------------------------------

class AuthenticationConfig(AppConfig):
    """
    Configuration class for the authentication application.
    Handles user registration, login, and token generation logic.
    """
    # Sets the default primary key type for all models in this app
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The full Python path to the application
    name = 'apps.authentication'