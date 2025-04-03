from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError


def validate_username(username):
    if User.objects.filter(username=username).exists():
        raise ValidationError("Esse nome de usuário já está em uso.")