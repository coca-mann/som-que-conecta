from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from backend.lessons.models import Lesson, Task, UserTask, TaskAditionalResource
from backend.lessons.serializers import LessonListSerializer, LessonDetailSerializer, UserTaskSerializer, TaskAditionalResourceSerializer
from backend.accounts.models import SKILL_LEVEL
from backend.instruments.models import InstrumentTypes


class SkillLevelsView(APIView):
    """
    View para listar os níveis de habilidade disponíveis.
    """
    def get(self, request):
        # Converte as tuplas do SKILL_LEVEL em dicionários com value e label
        levels = [{'value': value, 'label': label} for value, label in SKILL_LEVEL]
        return Response(levels)


class InstrumentTypesView(APIView):
    """
    View para listar os tipos de instrumentos disponíveis.
    """
    def get(self, request):
        instruments = InstrumentTypes.objects.all().values('id', 'name')
        # Formata os dados para o formato esperado pelo frontend
        formatted_instruments = [
            {'value': str(instrument['id']), 'label': instrument['name']}
            for instrument in instruments
        ]
        return Response(formatted_instruments)


# ViewSet para listar e ver detalhes dos Cursos (Lessons)
class LessonsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar e ver detalhes dos minicursos.
    A criação de cursos seria feita por um admin em outro lugar.
    """
    queryset = Lesson.objects.all().order_by('-created_at')
    # permission_classes = [IsAuthenticatedOrReadOnly] # Qualquer um pode ver
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['skill_level', 'instrument_type']
    ordering_fields = ['created_at', 'title', 'skill_level']
    ordering = ['-created_at']  # Ordenação padrão

    def get_serializer_class(self):
        """ Retorna um serializer diferente para a lista e para os detalhes. """
        if self.action == 'list':
            return LessonListSerializer
        return LessonDetailSerializer

    def get_serializer_context(self):
        """ Garante que o 'request' esteja disponível no contexto do serializer. """
        return {'request': self.request}

# ViewSet para as Tarefas (Tasks), focado nas ações do usuário
class TaskActionViewSet(viewsets.GenericViewSet):
    """
    ViewSet para realizar ações em tarefas, como marcar como concluída.
    """
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Marca uma tarefa como concluída para o usuário logado.
        Cria o registro em UserTask se for a primeira vez.
        """
        task = self.get_object()
        user = request.user

        # update_or_create é perfeito para isso:
        # - Se o registro já existe, ele atualiza.
        # - Se não existe, ele cria.
        user_task, created = UserTask.objects.update_or_create(
            user_id=user,
            task_id=task,
            defaults={'is_completed': True, 'date_completed': timezone.now()}
        )

        if created:
            return Response({'status': 'Tarefa concluída pela primeira vez'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'Tarefa marcada como concluída novamente'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def uncomplete(self, request, pk=None):
        """
        Desmarca uma tarefa como concluída para o usuário logado.
        """
        task = self.get_object()
        user = request.user

        try:
            user_task = UserTask.objects.get(user_id=user, task_id=task)
            user_task.is_completed = False
            user_task.date_completed = None
            user_task.save()
            return Response({'status': 'Tarefa desmarcada como concluída'}, status=status.HTTP_200_OK)
        except UserTask.DoesNotExist:
            return Response({'status': 'Tarefa não estava marcada como concluída'}, status=status.HTTP_200_OK)


class UserTaskViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar o progresso do usuário em todas as tarefas.
    Retorna apenas os registros UserTask pertencentes ao usuário autenticado.
    """
    serializer_class = UserTaskSerializer
    permission_classes = [IsAuthenticated] # SÓ usuários logados podem ver seu progresso

    def get_queryset(self):
        """
        Esta é a parte mais importante. Este método garante que a consulta
        seja filtrada para retornar APENAS os registros do usuário
        que está fazendo a requisição.
        """
        # self.request.user é o objeto do usuário autenticado
        return UserTask.objects.filter(user_id=self.request.user).select_related('task_id__lesson')


class TaskAditionalResourceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para visualizar recursos adicionais de tarefas.
    Apenas leitura, pois os recursos são gerenciados pelo admin.
    """
    serializer_class = TaskAditionalResourceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filtra os recursos adicionais por tarefa se um task_id for fornecido.
        """
        queryset = TaskAditionalResource.objects.all()
        task_id = self.request.query_params.get('task_id', None)
        
        if task_id is not None:
            queryset = queryset.filter(task_id=task_id)
            
        return queryset
