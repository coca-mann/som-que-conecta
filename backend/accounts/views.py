from rest_framework import viewsets, status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.contrib.auth import get_user_model
from backend.accounts.serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    ProfileSerializer,
    InProgressCourseSerializer,
    RecentActivitySerializer,
    UserGoalSerializer
)
from backend.lessons.models import Lesson, UserTask, Task
from backend.instruments.models import Instrument
from backend.accounts.models import UserHistory, UserGoals


User = get_user_model()

class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserDetailView(APIView):
    """
    View para obter os detalhes do usuário atualmente autenticado.
    """
    permission_classes = [IsAuthenticated] # Garante que apenas usuários logados acessem

    def get(self, request, *args, **kwargs):
        """
        Retorna os dados do usuário associado ao token JWT da requisição.
        """
        # O 'request.user' é o objeto do usuário logado, populado pelo DRF.
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Este método agora só busca o usuário. Simples e direto.
        """
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request):
        # A view não se preocupa mais com cálculos.
        user = self.get_object(request.user.pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        # A mágica agora acontece dentro do serializer.
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        """
        Atualiza parcialmente os dados do perfil do usuário autenticado.
        """
        # 3. A MESMA CORREÇÃO SE APLICA AQUI
        user = self.get_object(request.user.pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            # Retornamos o serializer com os dados atualizados (incluindo o counter)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class InProgressCourseListView(generics.ListAPIView):
    """
    Retorna uma lista de cursos (lições) que o usuário logado iniciou.
    """
    serializer_class = InProgressCourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 1. Pega o usuário logado
        user = self.request.user

        # 2. Descobre os IDs de todas as lições únicas que o usuário tem tarefas associadas
        in_progress_lesson_ids = UserTask.objects.filter(
            user_id=user
        ).values_list('task_id__lesson_id', flat=True).distinct()

        # 3. Retorna os objetos Lesson correspondentes a esses IDs
        return Lesson.objects.filter(pk__in=in_progress_lesson_ids).select_related('author')

    def get_serializer_context(self):
        """
        Garante que o 'request' seja passado para o serializer.
        Isso é crucial para que o get_progress() possa acessar o request.user.
        """
        return {'request': self.request}
    

class RecentActivityListView(generics.ListAPIView):
    serializer_class = RecentActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retorna as 20 atividades mais recentes do usuário logado
        return UserHistory.objects.filter(user=self.request.user).order_by('-created_at')[:20]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # --- Lógica de Otimização (Prefetch Manual) ---
        history_items = list(queryset)
        
        # 1. Agrupa os IDs por tipo de objeto
        object_ids_by_type = {}
        for item in history_items:
            object_ids_by_type.setdefault(item.object_name, set()).add(item.object_id)
            
        # 2. Busca todos os objetos relacionados em poucas queries
        prefetched_data = {}
        if 'Instrument' in object_ids_by_type:
            instruments = Instrument.objects.in_bulk(object_ids_by_type['Instrument'])
            prefetched_data['Instrument'] = instruments
            
        if 'Task' in object_ids_by_type:
            tasks = Task.objects.in_bulk(object_ids_by_type['Task'])
            prefetched_data['Task'] = tasks
        
        # Adicione outros modelos aqui se precisar (ex: Article)

        # 3. Passa os dados pré-buscados para o serializer através do contexto
        serializer_context = {'request': request, 'prefetched_data': prefetched_data}
        serializer = self.get_serializer(history_items, many=True, context=serializer_context)
        
        return Response(serializer.data)


class UserGoalViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite que as metas do usuário sejam visualizadas ou editadas.
    """
    serializer_class = UserGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Esta view deve retornar uma lista de todas as metas
        para o usuário autenticado atualmente.
        """
        return UserGoals.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Associa automaticamente a nova meta ao usuário logado ao salvar.
        """
        serializer.save(user=self.request.user)
