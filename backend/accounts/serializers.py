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
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def create(self, validated_data):
        """
        Sobrescreve o método create para usar create_user,
        que lida com o hashing da senha.
        """
        # Extrai os dados do dicionário validado
        email = validated_data.get('email')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')

        # Usa o método create_user do nosso CustomUserManager
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
            # Passe quaisquer outros campos aqui
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    """
    Serializador ajustado para refletir a nova estrutura de roles.
    """
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'first_name', 
            'last_name',
            'bio', 
            'profile_picture', 
            'birthday',
            'gender',
            'skill_level',
            'is_ong',
            'is_professor',
            'role',
        ]

    def get_role(self, obj):
        """
        Cria o valor para o campo 'role' baseado nos campos booleanos.
        'obj' é a instância do modelo User.
        """
        if obj.is_superuser or obj.is_staff:
            return 'admin'
        if obj.is_professor:
            return 'teacher'
        if obj.is_ong:
            return 'ong'
        return 'student'
