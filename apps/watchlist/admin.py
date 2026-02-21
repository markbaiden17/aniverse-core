from django.contrib import admin
from .models import WatchlistEntry


@admin.register(WatchlistEntry)
class WatchlistEntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'media_id', 'status', 'added_at']
    list_filter = ['status']
    search_fields = ['user__username', 'media_id']