from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from backend.accounts.models import User

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
    Customiza o fluxo de login social.
    """
    def pre_social_login(self, request, sociallogin):
        """
        Este método é chamado logo após o login social, mas antes de ser finalizado.
        É o local perfeito para conectar contas existentes.
        `sociallogin` contém os dados vindos do provedor (Google).
        """
        # Pega o usuário associado a esta conta social
        user = sociallogin.user
        
        # Se o usuário já existe no nosso sistema E não tem uma conta social já linkada...
        if user.id:
            return

        # Tenta encontrar um usuário local com o mesmo e-mail
        try:
            # Pega o e-mail vindo do Google
            email = sociallogin.account.extra_data['email'].lower()
            # Procura por um usuário local com este e-mail
            local_user = User.objects.get(email__iexact=email)

            # Se encontrou, conecta a conta social a este usuário local
            # e interrompe o fluxo de criação de um novo usuário.
            sociallogin.connect(request, local_user)

        except (User.DoesNotExist, KeyError, TypeError):
            # Se não encontrar um usuário local com esse e-mail,
            # ou se o e-mail não vier do Google (raro), segue o fluxo normal (criar uma nova conta).
            pass

    def save_user(self, request, sociallogin, form=None):
        """
        Este método é chamado para salvar o usuário, seja ele novo ou existente.
        Vamos usá-lo para atualizar os campos 'auth_provider' e 'sso_id'.
        """
        # Deixa a biblioteca fazer o trabalho pesado de salvar/associar o usuário
        user = super().save_user(request, sociallogin, form)

        # Atualiza nossos campos customizados
        user.auth_provider = 'GOOGLE'
        user.sso_id = sociallogin.account.uid # 'uid' é o ID único do usuário no Google
        
        # Garante que dados como nome e sobrenome vindos do Google sejam salvos
        # (isso evita que o nome seja sobrescrito se o usuário já existia)
        if not user.first_name and sociallogin.account.extra_data.get('given_name'):
            user.first_name = sociallogin.account.extra_data['given_name']
        if not user.last_name and sociallogin.account.extra_data.get('family_name'):
            user.last_name = sociallogin.account.extra_data['family_name']
        
        user.save()
        return user
