from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from backend.instruments.validators import validate_booking_conflict
from backend.core.utils import rename_and_upload_path


STATUS_CHOICES = [
        ('available', 'Disponível'),
        ('unavailable', 'Indisponível'),
        ('maintenance', 'Em Manutenção'),
    ]

STATUS_BOOKING = [
    ('PENDING', 'Pendente'),
    ('APPROVED', 'Aprovado'),
    ('REJECTED', 'Rejeitado'),
]


class InstrumentBrands(models.Model):
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        verbose_name='Nome',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descrição',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em',
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Marca de Instrumento'
        verbose_name_plural = 'Marcas de Instrumentos'


class InstrumentTypes(models.Model):
    name = models.CharField(
        null=False,
        blank=False,
        verbose_name='Nome'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descrição',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em',
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Tipo de Instrumento'
        verbose_name_plural = 'Tipos de Instrumentos'


class Instrument(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='Usuário'
    )
    type = models.ForeignKey(
        InstrumentTypes,
        on_delete=models.PROTECT,
        verbose_name='Tipo de Instrumento'
    )
    brand = models.ForeignKey(
        InstrumentBrands,
        on_delete=models.PROTECT,
        null=False,
        verbose_name='Marca'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name='Status'
    )
    featured = models.BooleanField(
        default=False,
        verbose_name='Destaque'
    )
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='Nome'
    )
    color = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Cor'
    )
    color_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Nome da Cor'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )
    is_available = models.BooleanField(
        default=False,
        verbose_name='Disponível'
    )
    is_loanable = models.BooleanField(
        default=False,
        verbose_name='Emprestável'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Localização'
    )
    availability = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Disponibilidade'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Modificado em'
    )

    def __str__(self):
        return f"{self.type.name} {self.color}"

    class Meta:
        verbose_name = 'Instrumento'
        verbose_name_plural = 'Instrumentos'


class InstrumentBookings(models.Model):
    instrument_id = models.ForeignKey(
        Instrument,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Instrumento'
    )
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuário que agendou'
    )
    reservation_date = models.DateField(
        blank=False,
        null=False,
        verbose_name='Data de agendamento'
    )
    reservation_starttime = models.TimeField(
        blank=True,
        null=True,
        verbose_name='Hora inicial do agendamento'
    )
    reservation_endtime = models.TimeField(
        blank=True,
        null=True,
        verbose_name='Hora final do agendamento'
    )
    status = models.CharField(
        choices=STATUS_BOOKING,
        blank=False,
        null=False,
        verbose_name='Status agendamento',
        default='PENDING'
    )
    reservation_refusal_reason = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Motivo da rejeição da reserva'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    def clean(self):
        # 1. Valida a lógica interna do próprio agendamento
        if self.reservation_starttime and self.reservation_endtime:
            if self.reservation_starttime >= self.reservation_endtime:
                raise ValidationError({
                    'reservation_endtime': 'O horário final do agendamento deve ser maior que o horário inicial.'
                })

        # 2. Chama o validador externo para checar conflitos com outros registros
        validate_booking_conflict(self)

    def save(self, *args, **kwargs):
        # A chamada full_clean() garante que o método clean() acima seja executado
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Reserva de instrumento'
        verbose_name_plural = 'Reservas de instrumentos'


class InstrumentPictures(models.Model):
    instrument_id = models.ForeignKey(Instrument, on_delete=models.CASCADE, null=True, verbose_name='Instrumento')
    picture = models.ImageField(upload_to=rename_and_upload_path('instruments_media/pictures/'), verbose_name='Foto')
