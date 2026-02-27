from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from .models import WatchlistEntry
from .serializers import WatchlistSerializer
from apps.reviews.permissions import IsOwnerOrReadOnly

# -----------------------------------------------------------------------------
# Watchlist Collection View (List & Create)
# -----------------------------------------------------------------------------

class WatchlistListCreateView(generics.ListCreateAPIView):
    """
    Handles listing a user's personal watchlist and adding new entries.
    Strictly restricted to authenticated users.
    """
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]
    
    # Enable sorting by date added, updated, or current status
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['added_at', 'updated_at', 'status']
    ordering = ['-added_at']

    def get_queryset(self):
        """
        Returns only the watchlist entries belonging to the current user.
        Supports optional filtering by the 'status' query parameter.
        """
        # Ensure users only see their own data
        queryset = WatchlistEntry.objects.filter(user=self.request.user)
        
        # Optional filter: /api/watchlist/?status=completed
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

# -----------------------------------------------------------------------------
# Individual Watchlist Entry View (Retrieve, Update, Delete)
# -----------------------------------------------------------------------------

class WatchlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles viewing, updating, or removing a specific watchlist item.
    Combines authentication and ownership checks for data security.
    """
    serializer_class = WatchlistSerializer
    # IsOwnerOrReadOnly ensures even authenticated users can't touch each other's lists
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        Limits the scope of the detail view to the current user's entries.
        """
        return WatchlistEntry.objects.filter(user=self.request.user)