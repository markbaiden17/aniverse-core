from rest_framework import serializers
from .models import WatchlistEntry
from .utils import get_anime_title

# -----------------------------------------------------------------------------
# Watchlist Serializer
# -----------------------------------------------------------------------------

class WatchlistSerializer(serializers.ModelSerializer):
    """
    Serializes WatchlistEntry instances into JSON data.
    Handles user-specific validation and automatic assignment of the user 
    to the entry upon creation.
    """
    # Provides the human-readable label from the Status TextChoices
    # e.g., returns "Plan to Watch" instead of "plan_to_watch"
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    # Fetches the anime title from AniList API based on media_id, with caching to reduce API calls
    media_title = serializers.SerializerMethodField()

    class Meta:
        model = WatchlistEntry
        fields = [
            'id',
            'media_id',
            'media_title',
            'status',
            'status_display',
            'added_at',
            'updated_at',
        ]
        # These fields are managed by the system and cannot be modified by the client
        read_only_fields = ['id', 'added_at', 'updated_at', 'media_title', 'status_display']

    def get_media_title(self, obj):
        """
        Fetches the anime title based on the media_id.
        In a real scenario, you'd call your AniList API wrapper here.
        """
        return get_anime_title(obj.media_id)

    def validate(self, data):
        """
        Custom validation to ensure a user doesn't add the same anime 
        to their watchlist multiple times.
        """
        request = self.context.get('request')
        if request and request.method == 'POST':
            media_id = data.get('media_id')
            # Check for existing entries for the current user and media_id
            if WatchlistEntry.objects.filter(user=request.user, media_id=media_id).exists():
                raise serializers.ValidationError(
                    {"media_id": "This title is already in your watchlist."}
                )
        return data

    def create(self, validated_data):
        """
        Intercepts the creation process to inject the authenticated user
        from the request context.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)