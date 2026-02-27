from django.urls import path
from .views import RegisterView, LoginView

# -----------------------------------------------------------------------------
# Authentication Route Definitions
# -----------------------------------------------------------------------------

urlpatterns = [
    # Endpoint for new user account creation
    path('register/', RegisterView.as_view(), name='auth-register'),
    
    # Endpoint for user credential validation and token retrieval
    path('login/', LoginView.as_view(), name='auth-login'),
]