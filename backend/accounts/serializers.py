from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
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
        user = User.objects.create_user(**validated_data)
        
        # 3. Geramos os tokens para o usuário recém-criado
        refresh = RefreshToken.for_user(user)
        
        # 4. Adicionamos os tokens ao objeto 'user' para que o serializer os inclua na resposta
        user.refresh = str(refresh)
        user.access = str(refresh.access_token)
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


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer para visualização e atualização do perfil do usuário logado.
    """
    # Usamos o campo 'get_gender_display' para retornar o nome legível ("Masculino")
    # em vez da chave ("M"). `source` aponta para o método do modelo.
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    
    # O campo 'role' que você já tinha é perfeito para o frontend.
    role = serializers.SerializerMethodField()
    lessons_counter = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'first_name', 
            'last_name',
            'profile_picture', # Este campo vai lidar com o upload
            'gender',
            'gender_display', # Campo extra para exibição no frontend
            'bio', 
            'birthday',
            'skill_level',
            # Campos booleanos para lógica de UI
            'is_ong',
            'is_professor',
            'role',
            'lessons_counter',
        ]
        read_only_fields = ['id', 'email', 'role', 'is_ong', 'is_professor']

    def get_role(self, obj):
        """
        Mantemos sua lógica para determinar o papel do usuário.
        """
        if obj.is_superuser or obj.is_staff:
            return 'admin'
        if obj.is_professor:
            return 'teacher'
        if obj.is_ong:
            return 'ong'
        return 'student'

    def update(self, instance, validated_data):
        # A lógica padrão de 'update' do ModelSerializer já trata
        # a atualização dos campos e do arquivo de imagem corretamente.
        return super().update(instance, validated_data)
