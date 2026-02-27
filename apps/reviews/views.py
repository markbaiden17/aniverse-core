from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly
from .utils import get_popular_anime

# -----------------------------------------------------------------------------
# Review Collection View (List & Create)
# -----------------------------------------------------------------------------

class ReviewListCreateView(generics.ListCreateAPIView):
    """
    Handles listing all reviews and creating new review entries.
    Supports searching by comment and ordering by rating or date.
    """
    # Optimized query using select_related to reduce database hits for user data
    queryset = Review.objects.select_related('user').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Enable DRF filtering and ordering capabilities
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['comment']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Optionally restricts the returned reviews to a given anime,
        by filtering against a `media_id` query parameter in the URL.
        """
        queryset = super().get_queryset()
        media_id = self.request.query_params.get('media_id')
        if media_id:
            try:
                queryset = queryset.filter(media_id=int(media_id))
            except ValueError:
                # Fallback if media_id is not a valid integer
                pass
        return queryset

# -----------------------------------------------------------------------------
# Individual Review View (Retrieve, Update, Delete)
# -----------------------------------------------------------------------------

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Handles operations on a single review instance.
    Enforces object-level permissions so only owners can edit/delete.
    """
    queryset = Review.objects.select_related('user').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# -----------------------------------------------------------------------------
# AniList Integration View
# -----------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def anime_list_view(request):
    """
    GET /api/reviews/anime-list/
    
    Fetches the top popular anime directly from the AniList GraphQL API.
    Provides an interface for users to discover content to review.
    """
    limit = request.query_params.get('limit', 20)
    try:
        limit = int(limit)
        # Cap the limit to respect AniList API rate limits
        if limit > 50:
            limit = 50  
    except ValueError:
        limit = 20
    
    # Execute external API fetch via utility function
    anime_list = get_popular_anime(limit)
    
    return Response({
        'count': len(anime_list),
        'results': anime_list
    })