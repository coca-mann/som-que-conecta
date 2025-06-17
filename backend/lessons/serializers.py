from rest_framework import serializers
from backend.lessons.models import (
    Lesson,
    Task,
    UserTask,
    TaskAditionalResource
)

# Um serializer auxiliar para mostrar detalhes da tarefa dentro do UserTask
class TaskForUserTaskSerializer(serializers.ModelSerializer):
    # Incluímos o ID e o título da lição para facilitar a navegação no frontend
    lesson_id = serializers.IntegerField(source='lesson.id', read_only=True)
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'order', 'lesson_id', 'lesson_title']


# O serializer principal para a lista de progresso do usuário
class UserTaskSerializer(serializers.ModelSerializer):
    # Usamos o serializer aninhado para mostrar os detalhes da tarefa
    task = TaskForUserTaskSerializer(source='task_id', read_only=True)

    class Meta:
        model = UserTask
        # Expondo os campos relevantes do UserTask
        fields = ['id', 'task', 'is_completed', 'date_completed']


# Serializer para os recursos adicionais de uma tarefa
class TaskAditionalResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAditionalResource
        fields = ['type', 'description', 'resource']

# Serializer para uma Tarefa (Task)
# Este é o serializer mais importante, pois ele verifica o status para o usuário logado
class TaskSerializer(serializers.ModelSerializer):
    resources = TaskAditionalResourceSerializer(many=True, read_only=True, source='taskaditionalresource_set')
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'order', 'video_url', 'content', 'resources', 'is_completed']

    def get_is_completed(self, obj):
        """
        Verifica se o usuário logado (vindo do contexto do request)
        já completou esta tarefa (obj).
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        
        # Procura por um registro em UserTask que conecte este usuário e esta tarefa
        return UserTask.objects.filter(user_id=user, task_id=obj, is_completed=True).exists()

# Serializer para a LISTA de Cursos (Lessons)
# Uma versão mais leve para a página principal de cursos.
class LessonListSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    instrument_type_name = serializers.CharField(source='instrument_type.name', read_only=True)
    skill_level_display = serializers.CharField(source='get_skill_level_display', read_only=True)
    duration_display = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'description', 'cover', 'instrument_type_name', 'skill_level', 
            'skill_level_display', 'tasks_count', 'author_name', 'progress', 'duration_display',
            'time_to_complete', 'type_time_to_complete'
        ]
        
    def get_duration_display(self, obj):
        """
        Retorna a duração formatada de forma legível.
        Ex: "2 meses" ou "1 dia"
        """
        if not obj.time_to_complete or not obj.type_time_to_complete:
            return ''
            
        type_map = {
            'D': 'dia' if obj.time_to_complete == 1 else 'dias',
            'M': 'mês' if obj.time_to_complete == 1 else 'meses',
            'Y': 'ano' if obj.time_to_complete == 1 else 'anos'
        }
        
        return f"{obj.time_to_complete} {type_map[obj.type_time_to_complete]}"
        
    def get_progress(self, obj):
        """
        Calcula o progresso do usuário logado neste curso (obj).
        """
        user = self.context['request'].user
        if not user.is_authenticated:
            return 0

        total_tasks = obj.task_set.count()
        if total_tasks == 0:
            return 0
        
        completed_tasks = UserTask.objects.filter(
            user_id=user, 
            task_id__lesson=obj, 
            is_completed=True
        ).count()
        
        return int((completed_tasks / total_tasks) * 100)

# Serializer para os DETALHES de um Curso (Lesson)
# Versão completa que inclui a lista de tarefas.
class LessonDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    instrument_type = serializers.StringRelatedField()
    tasks = TaskSerializer(many=True, read_only=True, source='task_set')

    class Meta:
        model = Lesson
        fields = '__all__'

    def get_author(self, obj):
        """
        Retorna o nome completo do autor da lição usando o método get_full_name().
        """
        return obj.author.get_full_name()
