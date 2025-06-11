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