from django.db.models import Avg, Count
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from apps.reviews.models import Review


class MediaStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, media_id):
        reviews = Review.objects.filter(media_id=media_id)

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

        aggregates = reviews.aggregate(
            average_rating=Avg('rating'),
            total_reviews=Count('id'),
        )

        distribution = {str(i): 0 for i in range(1, 11)}
        for entry in reviews.values('rating').annotate(count=Count('id')):
            distribution[str(entry['rating'])] = entry['count']

        return Response(
            {
                "media_id": media_id,
                "average_rating": round(aggregates['average_rating'], 2),
                "total_reviews": aggregates['total_reviews'],
                "rating_distribution": distribution,
            },
            status=status.HTTP_200_OK,
        )