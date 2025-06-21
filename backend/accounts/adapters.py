from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings

class AccountAdapter(DefaultAccountAdapter):
    """
    Adaptador para ações de contas locais (registro, login, reset de senha).
    Herdar do padrão já nos dá o método 'clean_email' e outros.
    """
    def save_user(self, request, user, form, commit=True):
        """
        Salva um novo usuário. Se for o primeiro usuário, o torna superusuário.
        """
        user = super().save_user(request, user, form, commit=False)
        user.is_active = True  # Ativa o usuário diretamente
        if commit:
            user.save()
        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Adaptador para ações de contas sociais (login com Google).
    """
    def save_user(self, request, sociallogin, form=None):
        """
        Salva um novo usuário vindo de um login social.
        """
        user = super().save_user(request, sociallogin, form)
        user.auth_provider = 'GOOGLE' # Marca o provedor de autenticação
        user.save()
        return user