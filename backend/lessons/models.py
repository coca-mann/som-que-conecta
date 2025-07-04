from django.db import models
from django.conf import settings
from backend.accounts.models import SKILL_LEVEL
from backend.instruments.models import InstrumentTypes
from backend.core.utils import rename_and_upload_path


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
    ('LINK', 'Link externo'),
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
        upload_to=rename_and_upload_path('lessons/cover/'),
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
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='lessons_created',
        blank=False,
        null=False,
        verbose_name='Usuário'
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
        return f"{self.title}"
    

class TaskAditionalResource(models.Model):
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
        upload_to=rename_and_upload_path('resource/files/'),
        blank=True,
        null=True,
        verbose_name='Arquivo'
    )
    resource_link = models.TextField(
        blank=True,
        null=True,
        verbose_name='Link'
    )
    
    def clean(self):
        from django.core.exceptions import ValidationError
        
        # Validação para garantir que pelo menos um dos campos (resource ou resource_link) está preenchido
        if not self.resource and not self.resource_link:
            raise ValidationError('É necessário fornecer um arquivo ou um link.')
        
        # Validação para garantir que não está tentando usar ambos os campos
        if self.resource and self.resource_link:
            raise ValidationError('Não é possível fornecer tanto um arquivo quanto um link. Escolha apenas um.')
        
        # Validação para garantir que o tipo corresponde ao recurso fornecido
        if self.type == 'LINK' and not self.resource_link:
            raise ValidationError('Para recursos do tipo Link, é necessário fornecer um link.')
        elif self.type != 'LINK' and not self.resource:
            raise ValidationError('Para recursos do tipo arquivo, é necessário fornecer um arquivo.')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.task_id.title} - {self.get_type_display()} - {self.description}"
    
    class Meta:
        verbose_name = 'Recurso Adicional'
        verbose_name_plural = 'Recursos Adicionais'
        ordering = ['task_id', 'id']
    

class UserTask(models.Model):
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