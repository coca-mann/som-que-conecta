from backend.accounts.models import UserHistory


def create_history_record(user, action, instance):
    """
    Cria um registro de histórico para uma determinada ação do usuário.

    :param user: A instância do usuário que realizou a ação.
    :param action: A string da ação (ex: 'CREATE_ARTICLE').
    :param instance: A instância do modelo sobre o qual a ação foi realizada.
    """
    UserHistory.objects.create(
        user=user,
        action=action,
        object_name=instance.__class__.__name__,  # Pega o nome do modelo (ex: 'Instrument')
        object_id=instance.pk,                    # Pega a chave primária do objeto
    )