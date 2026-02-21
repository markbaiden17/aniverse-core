from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from .models import WatchlistEntry
from .serializers import WatchlistSerializer
from apps.reviews.permissions import IsOwnerOrReadOnly


class WatchlistListCreateView(generics.ListCreateAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['added_at', 'updated_at', 'status']
    ordering = ['-added_at']

    def get_queryset(self):
        queryset = WatchlistEntry.objects.filter(user=self.request.user)
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class WatchlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WatchlistSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return WatchlistEntry.objects.filter(user=self.request.user)