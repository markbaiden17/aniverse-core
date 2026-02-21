from rest_framework import serializers
from .models import WatchlistEntry


class WatchlistSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = WatchlistEntry
        fields = [
            'id',
            'media_id',
            'status',
            'status_display',
            'added_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'added_at', 'updated_at']

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            media_id = data.get('media_id')
            if WatchlistEntry.objects.filter(user=request.user, media_id=media_id).exists():
                raise serializers.ValidationError(
                    {"media_id": "This title is already in your watchlist."}
                )
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)