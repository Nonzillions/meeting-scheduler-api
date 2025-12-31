
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'timezone',
                 'working_hours_start', 'working_hours_end']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extract password from validated data
        password = validated_data.pop('password', None)
        
        # Create user instance without password first
        user = User(**validated_data)
        
        # Set password using Django's proper method (hashes it)
        if password:
            user.set_password(password)
        
        # Save user to database
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user and user.is_active:
            # Return the authenticated user
            return user
        raise serializers.ValidationError("Invalid credentials")
