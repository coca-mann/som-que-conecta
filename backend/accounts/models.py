from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # Boa prática para referenciar o User model
from backend.accounts.managers import CustomUserManager

# Suas constantes GENDER_CHOICES, AUTH_PROVIDER, etc. continuam aqui...
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
    # ... etc
]


class UserType(models.Model):
    # Este modelo não muda, pois não tem relação direta com o User
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nome')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo de usuário'
        verbose_name_plural = 'Tipos de usuários'


# --- O NOVO MODELO DE USUÁRIO ---
class User(AbstractUser):
    # 1. Removemos o username e definimos o email como campo de login
    username = None
    email = models.EmailField('endereço de email', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] # Campos pedidos no 'createsuperuser'

    # 2. Movemos todos os campos do antigo UserProfile para cá
    user_type = models.ForeignKey(
        UserType,
        on_delete=models.PROTECT,
        null=True, # Torne nulo para facilitar a migração de dados
        blank=True,
        verbose_name='Tipo de Usuário',
    )
    birthday = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    bio = models.TextField(null=True, blank=True, verbose_name='Biografia')
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg', blank=True, verbose_name='Foto de Perfil')
    auth_provider = models.CharField(choices=AUTH_PROVIDER, blank=True, null=True, max_length=10, verbose_name='Provedor de autenticação')
    sso_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID de SSO')
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, null=True, max_length=1, verbose_name='Gênero')
    skill_level = models.CharField(choices=SKILL_LEVEL, blank=True, null=True, max_length=20, verbose_name='Nível de habilidade')
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


# O modelo UserProfile foi REMOVIDO.


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
    
    def __str__(self):
        return self.title

class UserHistory(models.Model):
    # 4. Apontamos a chave estrangeira para o novo modelo de usuário
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Usa a configuração do settings.py
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='history'
    )
    action = models.CharField(choices=HISTORY_ACTIONS, max_length=20, verbose_name='Ação')
    object = models.CharField(max_length=255, null=False, blank=False, verbose_name='Objeto')
    object_id = models.PositiveIntegerField(null=False, blank=False, verbose_name='ID do objeto')
    
    def __str__(self):
        return f"{self.user.email} - {self.action} - {self.object}"