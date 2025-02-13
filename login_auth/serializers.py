from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Student


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        """ Ensure email is unique """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class StudentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Student
    fields = ['id', 'stuname', 'email']