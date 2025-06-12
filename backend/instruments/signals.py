from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from backend.instruments.models import Instrument, InstrumentPictures
from backend.accounts.utils import create_history_record

@receiver(post_save, sender=Instrument)
def create_instrument_history(sender, instance, created, **kwargs):
    """
    Cria um registro de histórico quando um novo Instrumento é salvo.
    """
    if created:
        # A ação é executada pelo 'user_id' do instrumento
        create_history_record(
            user=instance.user_id, 
            action='ADD_INSTRUMENT', 
            instance=instance
        )
        
@receiver(post_delete, sender=InstrumentPictures)
def delete_picture_on_model_delete(sender, instance, **kwargs):
    """
    Escuta pelo sinal de exclusão de uma instância de InstrumentPictures e, em seguida,
    deleta o arquivo de imagem associado do sistema de arquivos.
    """
    # Verifica se a instância realmente tem um arquivo de imagem associado
    if instance.picture:
        # O método .delete() do campo de imagem cuida da exclusão do arquivo físico.
        # save=False é importante porque o modelo já foi deletado do banco de dados.
        instance.picture.delete(save=False)
        print(f"Arquivo de imagem deletado: {instance.picture.name}")
