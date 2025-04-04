from django.db import models
from django.contrib.auth.models import User
from backend.instruments.models import InstrumentTypes
from django_ckeditor_5.fields import CKEditor5Field


class LearningPaths(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='Nome')
    description = models.TextField(blank=True, verbose_name='Descrição')
    instrument_type_id = models.ForeignKey(InstrumentTypes, on_delete=models.SET_NULL, null=True, verbose_name='Tipo de Instrumento')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modificado em')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Caminho de aprendizado'
        verbose_name_plural = 'Caminhos de aprendizado'


class Lessons(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='Título')
    learning_path_id = models.ForeignKey(LearningPaths, on_delete=models.SET_NULL, null=True, verbose_name='Curso dessa lição')
    content = CKEditor5Field('Conteudo', config_name='extends')
    order = models.IntegerField(null=False, blank=False, verbose_name='Ordem')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modificado em')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Lição'
        verbose_name_plural = 'Lições'


class UserLearningProgress(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Usuário')
    learning_path_id = models.ForeignKey(LearningPaths, on_delete=models.SET_NULL, null=True, verbose_name='Curso')
    current_lesson_id = models.ForeignKey(Lessons, on_delete=models.SET_NULL, null=True, verbose_name='Lição atual')
    completed = models.BooleanField(verbose_name='Concluído')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de atualização')

    def __str__(self):
        learning_path_name = self.learning_path_id.name if self.learning_path_id else "Sem curso"
        lesson_name = self.current_lesson_id.title if self.current_lesson_id else "Sem lição"
        return f"{learning_path_name} - {lesson_name}"

    class Meta:
        verbose_name = 'Progresso de aprendizado do usuário'
        verbose_name_plural = 'Progresso de aprendizado dos usuários'
