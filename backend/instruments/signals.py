from django.db.models.signals import post_save
from django.dispatch import receiver
from backend.instruments.models import Instrument
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