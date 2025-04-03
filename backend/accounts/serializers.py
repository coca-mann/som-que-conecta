from django.contrib.auth.models import User
from rest_framework import serializers
from backend.accounts.models import UserProfile
from backend.accounts.validators import (
    validate_username,
    validate_email,
)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = '__all__'

    def validate_username(self, value):
        validate_username(value)
        return value

    def validate_email(self, value):
        validate_email(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile')

    class Meta:
        model = User
        fields = '__all__'
