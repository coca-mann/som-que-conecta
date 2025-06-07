from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outros'),
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
    ('CREATE', 'Criado'),
    ('UPDATE', 'Atualizado'),
    ('DELETE', 'Deletado'),
    ('STARTED', 'Iniciado'),
    ('COMPLETED', 'Concluído'),
    ('PUBLISHED', 'Publicado'),
]


class UserType(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        verbose_name='Nome',
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name='Descrição',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo de usuário'
        verbose_name_plural = 'Tipos de usuários'


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='profile'
    )
    user_type = models.ForeignKey(
        UserType,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name='Tipo de Usuário',
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Nascimento',
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='Biografia',
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='profile_pics/default.jpg',
        blank=True,
        verbose_name='Foto de Perfil',
    )
    auth_provider = models.CharField(
        choices=AUTH_PROVIDER,
        blank=True,
        null=True,
        verbose_name='Provedor de autenticação',
    )
    sso_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='ID de SSO',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em',
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Modificado em',
    )
    gender = models.CharField(
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        verbose_name='Gênero',
    )
    skill_level = models.CharField(
        choices=SKILL_LEVEL,
        blank=True,
        null=True,
        verbose_name='Nível de habilidade',
    )
    # modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'


class UserGoals(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='goals'
    )
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='Título',
    )
    description = models.TextField(
        null=False,
        blank=False,
        verbose_name='Descrição'
    )
    to_do_date = models.DateField(
        null=False,
        blank=False,
        verbose_name='Prazo',
    )
    
    def __str__(self):
        return self.title
    
class UserHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='history'
    )
    action = models.CharField(
        choices=HISTORY_ACTIONS,
        verbose_name='Ação'
    )
    object = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='Objeto'
    )
    object_id = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name='ID do objeto'
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.object}"