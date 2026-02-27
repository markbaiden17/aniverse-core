from django.urls import path
from .views import WatchlistListCreateView, WatchlistDetailView

# -----------------------------------------------------------------------------
# Watchlist Route Definitions
# -----------------------------------------------------------------------------

urlpatterns = [
    # Endpoint to view all items in the user's list or add a new anime to it
    path('', WatchlistListCreateView.as_view(), name='watchlist-list-create'),
    
    # Endpoint to update the status (e.g., move from 'Watching' to 'Completed')
    # or remove an entry from the list entirely via its primary key (pk)
    path('<int:pk>/', WatchlistDetailView.as_view(), name='watchlist-detail'),
]