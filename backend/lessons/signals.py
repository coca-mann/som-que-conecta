from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Task, Lesson

@receiver(post_save, sender=Task)
def update_tasks_count_on_save(sender, instance, created, **kwargs):
    """
    Este signal é chamado toda vez que uma Task é salva.
    Se a Task está sendo criada (created=True), ele incrementa o contador da Lesson.
    """
    if created:
        lesson = instance.lesson
        # Usamos F() para uma atualização atômica e segura no banco de dados.
        # Isso evita race conditions e é mais performático.
        Lesson.objects.filter(pk=lesson.pk).update(tasks_count=F('tasks_count') + 1)

@receiver(post_delete, sender=Task)
def update_tasks_count_on_delete(sender, instance, **kwargs):
    """
    Este signal é chamado toda vez que uma Task é deletada.
    Ele decrementa o contador da Lesson correspondente.
    """
    lesson = instance.lesson
    Lesson.objects.filter(pk=lesson.pk).update(tasks_count=F('tasks_count') - 1)