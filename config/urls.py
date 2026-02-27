"""
AniVerse API — Root URL Configuration
Maps the primary API namespaces to their respective application routes.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Administrative Interface
    path('admin/', admin.site.urls),
    
    # Authentication endpoints (Login, Register, Logout)
    path('api/auth/', include('apps.authentication.urls')),
    
    # Review management and public review feed
    path('api/reviews/', include('apps.reviews.urls')),
    
    # User-specific anime watchlists
    path('api/watchlist/', include('apps.watchlist.urls')),
    
    # Aggregated analytics and anime-specific statistics
    path('api/stats/', include('apps.stats.urls')),
]