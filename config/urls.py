from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/reviews/', include('apps.reviews.urls')),
    path('api/watchlist/', include('apps.watchlist.urls')),
    path('api/stats/', include('apps.stats.urls')),
]