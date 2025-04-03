from datetime import timedelta
from django.core.exceptions import ValidationError


def validate_booking_conflict(instance):
    if not instance.instrument_id or not instance.start_time:
        return

    end_time = instance.end_time or (instance.start_time + timedelta(hours=1))

    model_class = instance.__class__

    overlapping = model_class.objects.filter(
        instrument_id=instance.instrument_id,
        status__in=['PENDING', 'CONFIRM']
    ).exclude(id=instance.id).filter(
        start_time__lt=end_time,
        end_time__gt=instance.start_time
    )

    if overlapping.exists():
        raise ValidationError("Já existe uma reserva para esse instrumento neste período.")
