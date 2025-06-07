from django.db import models
from django.conf import settings
from backend.accounts.models import SKILL_LEVEL
from backend.instruments.models import InstrumentTypes


TYPE_TIMES = [
    ('D', 'Dias'),
    ('M', 'Meses'),
    ('Y', 'Anos'),
]


RESOURCE_TYPE = [
    ('DOCUMENT', 'Documento'),
    ('AUDIO', 'Audio'),
    ('VIDEO', 'Video'),
    ('IMAGE', 'Imagem'),
]


class Lesson(models.Model):
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='Título'
    )
    description = models.TextField(
        blank=False,
        null=False,
        verbose_name='Descrição'
    )
    cover = models.ImageField(
        upload_to='lessons/cover/',
        verbose_name='Capa'
    )
    instrument_type = models.ForeignKey(
        InstrumentTypes,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name='Tipo de instrumento'
    )
    skill_level = models.CharField(
        choices=SKILL_LEVEL,
        blank=False,
        null=False,
        verbose_name='Dificuldade'
    )
    time_to_complete = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name='Tempo estimado'
    )
    type_time_to_complete = models.CharField(
        choices=TYPE_TIMES,
        blank=False, 
        null=False,
        verbose_name='Tipo de tempo'
    )
    tasks_count = models.PositiveIntegerField(
        blank=False,
        default=0,
        verbose_name='Qtde tarefas'
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
        return self.title

    class Meta:
        verbose_name = 'Lição'
        verbose_name_plural = 'Lições'


class Task(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name='Lição'
    )
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='Título'
    )
    description = models.TextField(
        blank=False,
        null=False,
        verbose_name='Descrição'
    )
    order = models.IntegerField(
        blank=False,
        default=0,
        verbose_name='Ordem'
    )
    video_url = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name='Link do vídeo'
    )
    content = models.TextField(
        null=False,
        blank=False,
        verbose_name='Conteúdo'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Modificado em'
    )
    
    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
    
    def __str__(self):
        return f"{self.title} - {self.lesson_title}"
    

class TaksAditionalResource(models.Model):
    task_id = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Tarefa'
    )
    type = models.CharField(
        choices=RESOURCE_TYPE,
        blank=False,
        null=False,
        verbose_name='Tipo de recurso'
    )
    description = models.CharField(
        max_length=500,
        null=False,
        blank=False,
        verbose_name='Descrição'
    )
    resource = models.FileField(
        upload_to='resource/files/',
        blank=False,
        null=False,
        verbose_name='Arquivo'
    )
    
    def __str__(self):
        return f"{self.task_id_title} - {self.type} - {self.description}"
    
    
class UserTaks(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        blank=False,
        null=False,
        verbose_name='Usuário'
    )
    task_id = models.ForeignKey(
        Task,
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        verbose_name='Tarefa'
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name='Concluído'
    )
    date_completed = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Data e hora de conclusão'
    )