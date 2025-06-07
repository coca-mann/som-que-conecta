from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from backend.accounts.validators import (
    validate_username,
    validate_email,
    validate_auth_provider_sso_id,
    validate_date_of_birth,
    validate_profile_picture,
)

User = get_user_model()

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
        model = User
        exclude = ['user_type']

    def validate_auth_provider_sso_id(self, attrs):
        validate_auth_provider_sso_id(
            attrs.get("auth_provider"),
                      attrs.get("sso_id")
                      )
        return attrs
    
    def validate_date_of_birth(self, value):
        validate_date_of_birth(value)
        return value
    
    def validate_profile_picture(self, value):
        validate_profile_picture(value)
        return value


class UserWithProfileSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile')

    class Meta:
        model = User
        fields = '__all__'
