from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(CreateAPIView):
    """ Handles User Registration """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Ensure public access

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Custom behavior after user is created
        response.data = {
            'message': 'User registered successfully. Please check your email to verify your account.',
            'user': response.data}
        return response


class LoginView(APIView):
    """Handles user login."""
    permission_classes = [AllowAny]  # Ensure public access

    def post(self, request, *args, **kwargs):

        serializers = LoginSerializer(data=request.data)

        if serializers.is_valid():
            email = serializers.validated_data['username']  # username field contains email
            password = serializers.validated_data['password']

            # authentication through default django authentication
            user = authenticate(username=email, password=password)

            if user:
                login(request, user)   # for traditional session login
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            return Response({'details': "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)





@method_decorator(csrf_exempt, name='dispatch')  # 🚀 Disable CSRF for this view
class LogoutView(APIView):
    """
    Logout the user by deleting their authentication token.
    """
    permission_classes = [AllowAny]  # Ensure public access

    def post(self, request):
        token = request.headers.get("Authorization")  # Get token from headers
        if not token or not token.startswith("Token "):
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        token_key = token.split(" ")[1]  # Extract token value
        
        # Delete the token if it exists
        try:
            Token.objects.get(key=token_key).delete()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
