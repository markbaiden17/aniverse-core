from django.urls import path
from .views import MediaStatsView

# -----------------------------------------------------------------------------
# Statistics Route Definitions
# -----------------------------------------------------------------------------

urlpatterns = [
    # Endpoint for retrieving aggregated data for a specific anime
    # Example: /api/stats/1535/ (where 1535 is the media_id)
    path('<int:media_id>/', MediaStatsView.as_view(), name='media-stats'),
]