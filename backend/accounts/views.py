from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from django.contrib.auth import get_user_model
from backend.accounts.serializers import UserRegistrationSerializer, UserSerializer, ProfileSerializer


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
    """
    Endpoint para que o usuário logado possa visualizar e atualizar seu perfil.
    """
    permission_classes = [IsAuthenticated]

    # 1. Renomeamos para get_object e removemos o 'request' que não era usado
    def get_object(self, pk):
        """
        Busca o objeto User e anota com o campo extra.
        """
        try:
            # Atenção aqui: o nome do seu model é UserTaks, então a relação reversa
            # deve ser 'usertaks_set' ou o 'related_name' que você definiu.
            # Vou usar 'usertaks' como no seu código anterior.
            return User.objects.annotate(
                lessons_counter=Count('usertask__task_id__lesson', distinct=True)
            ).get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request):
        """
        Retorna os dados do perfil do usuário autenticado.
        """
        # 2. CHAMAMOS NOSSO MÉTODO get_object em vez de usar request.user
        user = self.get_object(request.user.pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
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