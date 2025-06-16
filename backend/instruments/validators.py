from datetime import timedelta
from django.core.exceptions import ValidationError


def validate_booking_conflict(instance):
    """
    Verifica se o intervalo de tempo de um agendamento (entre starttime e endtime)
    conflita com algum agendamento 'PENDING' ou 'APPROVED' existente
    para o mesmo instrumento e na mesma data.
    """
    # Se algum dos campos essenciais não estiver preenchido, não há como validar.
    if not all([
        instance.instrument_id, 
        instance.reservation_date, 
        instance.reservation_starttime, 
        instance.reservation_endtime
    ]):
        return

    model_class = instance.__class__

    # Busca por agendamentos que se sobrepõem no tempo
    conflicting_bookings = model_class.objects.filter(
        instrument_id=instance.instrument_id,
        reservation_date=instance.reservation_date,
        status__in=['PENDING', 'APPROVED'],
        # A condição de sobreposição de intervalos:
        # O horário de início do agendamento existente é ANTES do fim do novo agendamento.
        reservation_starttime__lt=instance.reservation_endtime,
        # E o horário de fim do agendamento existente é DEPOIS do início do novo agendamento.
        reservation_endtime__gt=instance.reservation_starttime,
    )

    # Se estiver atualizando um agendamento, exclua-o da verificação
    if instance.pk:
        conflicting_bookings = conflicting_bookings.exclude(pk=instance.pk)

    # Se a consulta encontrar algum resultado, há um conflito.
    if conflicting_bookings.exists():
        raise ValidationError(
            'Já existe um agendamento para este instrumento que conflita com este horário.'
        )