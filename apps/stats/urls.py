from django.urls import path
from .views import MediaStatsView

urlpatterns = [
    path('<int:media_id>/', MediaStatsView.as_view(), name='media-stats'),
]