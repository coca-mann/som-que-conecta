from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Article
from .services import article_validation_service

@receiver(pre_save, sender=Article)
def validate_article_with_ai(sender, instance, **kwargs):
    """
    Signal que valida o artigo com IA quando ele é enviado para publicação
    """
    # Se for uma atualização, pega a instância antiga
    if instance.pk:
        try:
            old_instance = Article.objects.get(pk=instance.pk)
            # Se já estiver publicado e não estiver mudando o status, não precisa validar
            if old_instance.is_published and instance.is_published:
                return
        except Article.DoesNotExist:
            old_instance = None
    else:
        old_instance = None

    # Verifica se o artigo está sendo enviado para publicação
    if instance.is_published and not instance.is_draft:
        # Se já foi revisado e aprovado pela IA, apenas define a data de publicação
        if instance.is_reviewed and instance.ai_bool:
            instance.published_at = timezone.now()
            return

        # Realiza a validação com IA
        validation_result = article_validation_service.validate_article(instance.content)
        
        if validation_result['is_valid']:
            # Atualiza o feedback da IA
            instance.ai_feedback = validation_result['feedback']
            instance.ai_bool = validation_result['is_approved']
            
            # Define o status de revisão e moderação
            instance.is_reviewed = True
            instance.is_moderated = True
            
            if validation_result['is_approved']:
                # Se aprovado, mantém como publicado e define a data de publicação
                instance.is_published = True
                instance.published_at = timezone.now()
            else:
                # Se não aprovado, volta para rascunho
                instance.is_published = False
                instance.is_draft = True
                instance.publishing_refused_reason = validation_result['feedback']
        else:
            # Se houver erro na validação, mantém como rascunho
            instance.is_published = False
            instance.is_draft = True
            instance.publishing_refused_reason = f"Erro na validação por IA: {validation_result['error']}" 