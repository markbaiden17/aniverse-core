from django.db.models import Avg, Count
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from apps.reviews.models import Review

# -----------------------------------------------------------------------------
# Media Statistics View
# -----------------------------------------------------------------------------

class MediaStatsView(APIView):
    """
    API endpoint that calculates and returns aggregated statistics for a specific anime.
    Computes average ratings and the frequency distribution of scores (1-10).
    """
    permission_classes = [AllowAny]

    def get(self, request, media_id):
        """
        Handle GET requests to retrieve statistical data for a given media_id.
        """
        # Filter reviews for the specific anime title
        reviews = Review.objects.filter(media_id=media_id)

        # Handle the case where no reviews exist yet for this title
        if not reviews.exists():
            return Response(
                {
                    "media_id": media_id,
                    "average_rating": None,
                    "total_reviews": 0,
                    "rating_distribution": {str(i): 0 for i in range(1, 11)},
                    "detail": "No reviews found for this title.",
                },
                status=status.HTTP_200_OK,
            )

        # Perform database-level aggregation for average and count
        aggregates = reviews.aggregate(
            average_rating=Avg('rating'),
            total_reviews=Count('id'),
        )

        # Initialize a dictionary for the 1-10 rating distribution
        distribution = {str(i): 0 for i in range(1, 11)}
        
        # Annotate and count occurrences for each rating value
        for entry in reviews.values('rating').annotate(count=Count('id')):
            distribution[str(entry['rating'])] = entry['count']

        # Return formatted statistical payload
        return Response(
            {
                "media_id": media_id,
                "average_rating": round(aggregates['average_rating'], 2),
                "total_reviews": aggregates['total_reviews'],
                "rating_distribution": distribution,
            },
            status=status.HTTP_200_OK,
        )