from django.db import models
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
    ('O', 'Outros'),
]

AUTH_PROVIDER = [
    ('local', 'Autenticação local'),
    ('google', 'Autenticação SSO Google'),
]


class UserType(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Nome')
    description = models.TextField(null=True, blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modificado em')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo de usuário'
        verbose_name_plural = 'Tipos de usuários'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    user_type = models.ForeignKey(UserType, on_delete=models.PROTECT, null=False, blank=False, verbose_name='Tipo de Usuário')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Data de Nascimento')
    bio = models.TextField(null=True, blank=True, verbose_name='Biografia')
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg', blank=True, verbose_name='Foto de Perfil')
    auth_provider = models.CharField(choices=AUTH_PROVIDER, blank=True, null=True, verbose_name='Provedor de autenticação')
    sso_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID de SSO')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modificado em')
    gender = models.CharField(choices=GENDER_CHOICES, blank=True, null=True, verbose_name='Gênero')
    # modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = 'Perfil de Usuário'
        verbose_name_plural = 'Perfis de Usuários'
