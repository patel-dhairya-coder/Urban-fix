from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Complaint

# --- A simplified User Serializer for nesting ---
class BasicUserSerializer(serializers.ModelSerializer):
    """
    A simplified serializer to represent the user in nested relationships.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# --- User Serializer for Registration ---
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create and return a new user with a hashed password.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# --- Complaint Serializer (Updated) ---
class ComplaintSerializer(serializers.ModelSerializer):
    """
    Serializer for the Complaint model.
    """
    # Use a method to get the human-readable name for the category
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    # Nest the BasicUserSerializer to show user details
    user = BasicUserSerializer(read_only=True)

    class Meta:
        model = Complaint
        fields = [
            'id', 
            'report_id', 
            'user', # Now shows a nested user object
            'category', 
            'category_display', # Shows the readable category name
            'location', 
            'description', 
            'photo', 
            'latitude', 
            'longitude', 
            'status', 
            'submitted_at'
        ]
        # user is now a nested object, so it's inherently read-only here
        read_only_fields = ['status', 'report_id', 'submitted_at']