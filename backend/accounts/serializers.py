from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from backend.accounts.validators import (
    validate_username,
    validate_email,
    validate_auth_provider_sso_id,
    validate_date_of_birth,
    validate_profile_picture,
)
from backend.lessons.models import Lesson, UserTask

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
    lessons_counter = serializers.SerializerMethodField(read_only=True)
    completed_tasks_counter = serializers.SerializerMethodField()
    instruments_counter = serializers.SerializerMethodField()
    
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
            'completed_tasks_counter',
            'instruments_counter',
        ]
        read_only_fields = ['id', 'email', 'role', 'is_ong', 'is_professor']
        
    def get_lessons_counter(self, obj):
        result = obj.usertask_set.aggregate(
            total_lessons=Count('task_id__lesson', distinct=True)
        )
        return result['total_lessons']
    
    def get_completed_tasks_counter(self, obj):
        """
        Cálculo ISOLADO para o contador de tarefas completas.
        'obj' aqui é a instância do usuário (User).
        """
        return obj.usertask_set.filter(is_completed=True).count()
    
    def get_instruments_counter(self, obj):
        result = obj.instrument_set.aggregate(total_instrument=Count('user_id__instrument'))
        return result['total_instrument']

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


class InProgressCourseSerializer(serializers.ModelSerializer):
    """
    Serializer para a lista de cursos em andamento do usuário.
    """
    # Campo para o nome do instrutor, buscando o nome completo do autor
    instructor_name = serializers.CharField(source='author.get_full_name', read_only=True)
    
    # Campo calculado para o progresso
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',           # Nome do curso
            'cover',           # Imagem de capa
            'instructor_name', # Nome do instrutor
            'progress',        # Progresso em porcentagem
        ]

    def get_progress(self, obj):
        """
        Calcula o progresso do usuário na lição (curso).
        'obj' é a instância de Lesson.
        """
        # Para acessar o 'request.user', precisamos que ele seja passado no contexto pela view
        user = self.context['request'].user

        # 1. Pega o total de tarefas que esta lição possui
        total_tasks = obj.tasks_count
        if total_tasks == 0:
            return 0 # Evita divisão por zero se a lição não tiver tarefas

        # 2. Conta quantas tarefas DESTA lição o usuário CONCLUIU
        completed_tasks = UserTask.objects.filter(
            task_id__lesson=obj,  # Filtra tarefas da lição atual
            user_id=user,         # Filtra para o usuário logado
            is_completed=True
        ).count()

        # 3. Calcula a porcentagem
        progress_percentage = (completed_tasks / total_tasks) * 100
        return int(progress_percentage) # Retorna como um inteiro (ex: 75)
