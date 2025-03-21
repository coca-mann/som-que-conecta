from django.db import models
from django.contrib.auth.models import User

STATUS_BOOKING = [
    ('PENDING', 'Pendente'),
    ('CONFIRM', 'Confirmado'),
    ('CANCELED', 'Cancelado'),
]

class InstrumentBrands(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

class InstrumentTypes(models.Model):
    name = models.CharField(null=False, blank=False)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    
class UserInstrument(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    instrument_type_id = models.ForeignKey(InstrumentTypes, on_delete=models.PROTECT)
    color = models.CharField(max_length=50, blank=True, null=True)
    brand_id = models.ForeignKey(InstrumentBrands, on_delete=models.PROTECT, null=False)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.instrument_type_id.name} {self.color}"
    

class InstrumentAvailability(models.Model):
    instrument_id = models.ForeignKey(UserInstrument, on_delete=models.SET_NULL, null=True, verbose_name='Instrumento')
    available_from = models.DateTimeField(null=False, blank=False, verbose_name='Disponível desde')
    available_to = models.DateTimeField(null=True, blank=True, verbose_name='Disponível até')
    recurring = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class InstrumentBookings(models.Model):
    instrument_id = models.ForeignKey(UserInstrument, on_delete=models.SET_NULL, null=True, verbose_name='Instrumento')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Usuário que agendou')
    start_time = models.DateTimeField(blank=False, null=False, verbose_name='Inicio agendamento')
    end_time = models.DateTimeField(blank=True, null=True, verbose_name='Fim agendamento')
    status = models.CharField(choices=STATUS_BOOKING, blank=False, null=False, verbose_name='Status agendamento')
    expires_at = models.DateTimeField(blank=True, null=True, verbose_name='Limite para confirmar agendamento')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)