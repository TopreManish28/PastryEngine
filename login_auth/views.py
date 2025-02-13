from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer,StudentSerializer
from .models import Student
from rest_framework.permissions import AllowAny, IsAuthenticated


# Create your views here.

class RegisterView(CreateAPIView):
    """ Handles User Registration """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  # Allow anyone to access this view

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Custom behavior after user is created
        response.data = {'message': 'User registered successfully. Please check your email to verify your account.'}
        return response
    

class StudentList(ListAPIView):
  queryset = Student.objects.all()
  serializer_class = StudentSerializer
  permission_classes = [AllowAny]  # Allow anyone to access this view


