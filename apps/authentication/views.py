from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, LoginSerializer

# -----------------------------------------------------------------------------
# User Registration View
# -----------------------------------------------------------------------------

class RegisterView(APIView):
    """
    API endpoint for new user registration.
    Allows any user to create an account and returns an auth token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Handle POST requests to create a new user."""
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the new user and generate/retrieve their unique token
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response(
                {
                    "message": "Account created successfully.",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    "token": token.key,
                },
                status=status.HTTP_201_CREATED,
            )
        
        # Return validation errors (e.g., username taken, password too short)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# -----------------------------------------------------------------------------
# User Login View
# -----------------------------------------------------------------------------

class LoginView(APIView):
    """
    API endpoint for user authentication.
    Validates credentials and returns a persistent auth token.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Handle POST requests for user authentication."""
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            # Retrieve the user object validated by the serializer
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            
            return Response(
                {
                    "message": "Login successful.",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    "token": token.key,
                },
                status=status.HTTP_200_OK,
            )
        
        # Return validation errors (e.g., invalid credentials)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)