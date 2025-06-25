import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from backend.core.utils import rename_and_upload_path
from backend.accounts.managers import CustomUserManager


GENDER_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outros'),
    ('N', 'Prefiro não informar'),
]

AUTH_PROVIDER = [
    ('LOCAL', 'Autenticação local'),
    ('GOOGLE', 'Autenticação SSO Google'),
]

SKILL_LEVEL = [
    ('BEGINNER', 'Iniciante'),
    ('INTERMEDIATE', 'Intermediário'),
    ('ADVANCED', 'Avançado'),
]

HISTORY_ACTIONS = [
    ('CREATE', 'Criou'),
    ('UPDATE', 'Atualizou'),
    ('DELETE', 'Deletou'),
    ('START_LESSON', 'Iniciou a lição'),
    ('COMPLETE_LESSON', 'Concluiu a lição'),
    ('COMPLETE_TASK', 'Concluiu a tarefa'),
    ('ADD_INSTRUMENT', 'Adicionou o instrumento'),
    ('CREATE_ARTICLE', 'Publicou o artigo'),
    ('POST_COMMENT', 'Comentou em'),
]


class User(AbstractUser):
    # 1. Removemos o username e definimos o email como campo de login
    username = None
    email = models.EmailField('endereço de email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] # Campos pedidos no 'createsuperuser'

    # 2. Movemos todos os campos do antigo UserProfile para cá
    birthday = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    bio = models.TextField(null=True, blank=True, verbose_name='Biografia')
    profile_picture = models.ImageField(
        upload_to=rename_and_upload_path('profile_pics/'),
        default='profile_pics/default.jpg',
        blank=True,
        verbose_name='Foto de Perfil'
    )
    auth_provider = models.CharField(choices=AUTH_PROVIDER, blank=True, null=True, max_length=10, verbose_name='Provedor de autenticação')
    sso_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID de SSO')
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, null=True, max_length=1, verbose_name='Gênero')
    skill_level = models.CharField(choices=SKILL_LEVEL, default='BEGINNER', max_length=20, verbose_name='Nível de habilidade')
    is_ong = models.BooleanField(default=False, verbose_name='Usuário ONG')
    is_professor = models.BooleanField(default=False, verbose_name='Professor')
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email

    def update_skill_level(self):
        """
        Atualiza o nível de habilidade do usuário baseado no número de cursos concluídos.
        Um curso é considerado concluído quando todas as suas tarefas foram completadas.
        """
        from django.db.models import Count, Q
        from backend.lessons.models import UserTask, Task

        # Conta quantos cursos únicos o usuário completou
        completed_courses = UserTask.objects.filter(
            user_id=self,
            is_completed=True
        ).values('task_id__lesson').distinct().count()

        # Atualiza o nível de habilidade baseado no número de cursos
        if completed_courses >= 6:
            self.skill_level = 'ADVANCED'
        elif completed_courses >= 3:
            self.skill_level = 'INTERMEDIATE'
        else:
            self.skill_level = 'BEGINNER'
        
        self.save()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class UserGoals(models.Model):
    # 3. Apontamos a chave estrangeira para o novo modelo de usuário
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Usa a configuração do settings.py
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='goals'
    )
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='Título')
    description = models.TextField(null=False, blank=False, verbose_name='Descrição')
    to_do_date = models.DateField(null=False, blank=False, verbose_name='Prazo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Meta do Usuário'
        verbose_name_plural = 'Metas dos Usuários'


class UserHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='history'
    )
    action = models.CharField(choices=HISTORY_ACTIONS, max_length=20, verbose_name='Ação')
    # O campo 'object' foi renomeado para 'object_name' para evitar conflito com a palavra reservada 'object'
    object_name = models.CharField(max_length=255, null=False, blank=False, verbose_name='Nome do Objeto')
    object_id = models.PositiveIntegerField(null=False, blank=False, verbose_name='ID do objeto')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ocorrido em')
    
    def __str__(self):
        return f"{self.user.email} - {self.get_action_display()} - {self.object_name}"

    class Meta:
        verbose_name = 'Histórico do Usuário'
        verbose_name_plural = 'Históricos dos Usuários'
        ordering = ['-created_at']


class EmailVerificationToken(models.Model):
    # Usamos UUID para tokens seguros e únicos
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Ligação com o usuário que precisa ser verificado
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Data de criação para calcular a expiração
    created_at = models.DateTimeField(auto_now_add=True)
    
    def is_expired(self):
        # Define que o token expira em 1 hora (ajuste conforme necessário)
        return self.created_at < timezone.now() - timedelta(hours=1)

    class Meta:
        verbose_name = 'Token de Verificação de Email'
        verbose_name_plural = 'Tokens de Verificação de Email'

