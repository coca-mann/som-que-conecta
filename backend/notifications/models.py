from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

NOTIFICATION_TYPE = [
    ('BOOKING', 'Agendamento'),
    ('CANCELING', 'Cancelamento'),
    ('REMINDER', 'Lembrete'),
    ('MARKETING', 'Marketing'),
    ('IMPORTANT', 'Importante'),
]

class Notifications(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Destinatário')
    message = CKEditor5Field('Conteudo', config_name='extends')
    type = models.CharField(choices=NOTIFICATION_TYPE, blank=False, verbose_name='Tipo de notificação')
    is_read = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)