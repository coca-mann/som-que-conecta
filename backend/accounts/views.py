from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from backend.accounts.serializers import UserRegistrationSerializer, UserSerializer


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