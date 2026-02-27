from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers

# -----------------------------------------------------------------------------
# User Registration Serializer
# -----------------------------------------------------------------------------

class RegisterSerializer(serializers.ModelSerializer):
    """
    Handles the validation and creation of new user accounts.
    Enforces password security and unique username constraints.
    """
    # Password field is write-only to ensure it is never returned in API responses
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def validate_username(self, value):
        """Check if the chosen username is already taken."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def create(self, validated_data):
        """Create a new User instance using the set_password hashing method."""
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user

# -----------------------------------------------------------------------------
# User Login Serializer
# -----------------------------------------------------------------------------

class LoginSerializer(serializers.Serializer):
    """
    Validates user credentials for authentication.
    Does not persist data but verifies it against existing User records.
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticate credentials and return the user object if valid."""
        user = authenticate(username=data['username'], password=data['password'])
        
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
            
        # Store the authenticated user in the validated data dictionary
        data['user'] = user
        return data