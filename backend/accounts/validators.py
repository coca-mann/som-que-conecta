import datetime
from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError


def validate_username(username):
    if User.objects.filter(username=username).exists():
        raise ValidationError("Esse nome de usuário já está em uso.")
  

def validate_email(email):
    if User.objects.filter(email=email).exists():
        raise ValidationError("Um usuário com essa conta de e-mail já existe")


def validate_auth_provider_sso_id(auth_provider, sso_id):
    if auth_provider == 'google' and not sso_id:
        raise ValidationError("O campo sso_id é obrigatório quando o provedor de autenticação é Google.")
    

def validate_date_of_birth(date_of_birth):
    if date_of_birth > datetime.date.today():
        raise ValidationError("Data de Nascimento não pode ser no futuro!")


def validate_profile_picture(file):
    max_size = 2 * 1024 * 1024

    if hasattr(file, 'content_type'):
        if not file.content_type.startswith("image/"):
            raise ValidationError("O arquivo deve ser uma imagem válida.")
        
        if file.size > max_size:
            raise ValidationError("A imagem deve ter no máximo 2MB.")
