from django.db.models import F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from backend.lessons.models import Task, Lesson, UserTask
from backend.accounts.utils import create_history_record

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


@receiver(post_save, sender=UserTask)
def create_task_completion_history(sender, instance, created, **kwargs):
    """
    Cria um registro de histórico quando uma UserTask é marcada como concluída.
    """
    # Verificamos se 'is_completed' está True e se não é um objeto recém-criado.
    # O ideal é checar se o campo 'is_completed' realmente mudou,
    # mas para simplificar, vamos registrar na primeira vez que for salvo como True.
    if instance.is_completed:
        # Para evitar registros duplicados se o objeto for salvo várias vezes
        # já estando completo, podemos fazer uma verificação.
        history_exists = instance.user_id.history.filter(
            action='COMPLETE_TASK', 
            object_name='UserTask', 
            object_id=instance.pk
        ).exists()

        if not history_exists:
            create_history_record(
                user=instance.user_id,
                action='COMPLETE_TASK',
                instance=instance.task_id # O objeto de interesse é a Tarefa, não o registro UserTask
            )