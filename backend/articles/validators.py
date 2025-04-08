from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError


def validate_user_can_post_article(user):
    if not user or not user.is_authenticated:
        raise ValidationError("Usuário não autenticado.")

    try:
        user_type = user.userprofile.user_type
    except AttributeError:
        raise ValidationError("Perfil de usuário inválido ou inexistente.")

    if user_type not in [2, 3]:
        raise ValidationError("Você não tem permissão para criar artigos.")
