from rest_framework import serializers
from .models import Review
from .utils import get_anime_title

# -----------------------------------------------------------------------------
# Review ModelSerializer
# -----------------------------------------------------------------------------

class ReviewSerializer(serializers.ModelSerializer):
    """
    Transforms Review model instances into JSON and handles data validation.
    Integrates external data from AniList and enforces per-user constraints.
    """
    # Flattens the username for easier consumption by front-end clients
    username = serializers.ReadOnlyField(source='user.username')
    
    # Dynamic field to fetch titles from the AniList API based on media_id
    anime_title = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            'username',
            'media_id',
            'anime_title',
            'rating',
            'comment',
            'created_at',
            'updated_at',
        ]
        # Prevents these fields from being modified via POST or PATCH requests
        read_only_fields = ['id', 'user', 'username', 'created_at', 'updated_at']

    def get_anime_title(self, obj):
        """
        Retrieves the anime title from the AniList API using the media_id.
        Calls the utility function to perform the external request.
        """
        return get_anime_title(obj.media_id)

    def validate_rating(self, value):
        """Ensures the rating adheres to the 1-10 numerical scale."""
        if not (1 <= value <= 10):
            raise serializers.ValidationError("Rating must be an integer between 1 and 10.")
        return value

    def validate(self, data):
        """
        Object-level validation to prevent duplicate reviews by the same user 
        for a specific media title during creation.
        """
        request = self.context.get('request')
        if request and request.method == 'POST':
            media_id = data.get('media_id')
            if Review.objects.filter(user=request.user, media_id=media_id).exists():
                raise serializers.ValidationError(
                    {"media_id": "You have already submitted a review for this title."}
                )
        return data

    def create(self, validated_data):
        """
        Overrides the creation process to automatically assign 
        the current authenticated user to the review instance.
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)