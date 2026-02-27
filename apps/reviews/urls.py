from django.urls import path
from .views import ReviewListCreateView, ReviewDetailView, anime_list_view

# -----------------------------------------------------------------------------
# Review App Route Definitions
# -----------------------------------------------------------------------------

urlpatterns = [
    # Endpoint for listing all reviews or creating a new review entry
    path('', ReviewListCreateView.as_view(), name='review-list-create'),
    
    # Endpoint for retrieving, updating, or deleting a specific review by its ID
    path('<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    
    # Specialized endpoint to fetch a curated list of anime titles from AniList
    path('anime-list/', anime_list_view, name='anime-list'),
]