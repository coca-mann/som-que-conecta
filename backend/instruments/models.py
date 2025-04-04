from django.db import models
from django.contrib.auth.models import User
from backend.instruments.validators import validate_booking_conflict


STATUS_BOOKING = [
    ('PENDING', 'Pendente'),
    ('CONFIRM', 'Confirmado'),
    ('CANCELED', 'Cancelado'),
]


class InstrumentBrands(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nome')
    description = models.TextField(blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modificado em')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Marca de Instrumento'
        verbose_name_plural = 'Marcas de Instrumentos'


class InstrumentTypes(models.Model):
    name = models.CharField(null=False, blank=False, verbose_name='Nome')
    description = models.TextField(blank=True, verbose_name='Descrição')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modificado em')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Tipo de Instrumento'
        verbose_name_plural = 'Tipos de Instrumentos'


class UserInstrument(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Usuário')
    instrument_type_id = models.ForeignKey(InstrumentTypes, on_delete=models.PROTECT, verbose_name='Tipo de Instrumento')
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name='Cor')
    brand_id = models.ForeignKey(InstrumentBrands, on_delete=models.PROTECT, null=False, verbose_name='Marca')
    description = models.TextField(blank=True, verbose_name='Descrição')
    is_available = models.BooleanField(blank=True, verbose_name='Disponível')
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name='Localização')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modificado em')

    def __str__(self):
        return f"{self.instrument_type_id.name} {self.color}"

    class Meta:
        verbose_name = 'Instrumento'
        verbose_name_plural = 'Instrumentos'


class InstrumentAvailability(models.Model):
    instrument_id = models.ForeignKey(UserInstrument, on_delete=models.SET_NULL, null=True, verbose_name='Instrumento')
    available_from = models.DateTimeField(null=False, blank=False, verbose_name='Disponível desde')
    available_to = models.DateTimeField(null=True, blank=True, verbose_name='Disponível até')
    recurring = models.BooleanField(verbose_name='Recorrente')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modificado em')

    class Meta:
        verbose_name = 'Disponibilidade de instrumento'
        verbose_name_plural = 'Disponibilidades de instrumentos'


class InstrumentBookings(models.Model):
    instrument_id = models.ForeignKey(UserInstrument, on_delete=models.SET_NULL, null=True, verbose_name='Instrumento')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Usuário que agendou')
    start_time = models.DateTimeField(blank=False, null=False, verbose_name='Inicio agendamento')
    end_time = models.DateTimeField(blank=True, null=True, verbose_name='Fim agendamento')
    status = models.CharField(choices=STATUS_BOOKING, blank=False, null=False, verbose_name='Status agendamento')
    expires_at = models.DateTimeField(blank=True, null=True, verbose_name='Limite para confirmar agendamento')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modificado em')

    def clean(self):
        validate_booking_conflict(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Reserva de instrumento'
        verbose_name_plural = 'Reservas de instrumentos'
