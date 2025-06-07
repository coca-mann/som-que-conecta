from rest_framework.serializers import ValidationError
from backend.accounts.models import User


def validate_user_can_post_article(user):


    if not user or not user.is_authenticated:
        raise ValidationError("Usuário não autenticado.")

    profile = User.objects.filter(id=user).first()

    if not profile:
        raise ValidationError("Perfil de usuário não encontrado.")

    if profile.user_type.id not in [2, 3]:
        raise ValidationError("Você não tem permissão para criar artigos.")
