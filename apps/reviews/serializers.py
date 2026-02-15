from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = [
            'id',
            'user',
            'username',
            'media_id',
            'rating',
            'comment',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'username', 'created_at', 'updated_at']

    def validate_rating(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError("Rating must be an integer between 1 and 10.")
        return value

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            media_id = data.get('media_id')
            if Review.objects.filter(user=request.user, media_id=media_id).exists():
                raise serializers.ValidationError(
                    {"media_id": "You have already submitted a review for this title."}
                )
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)