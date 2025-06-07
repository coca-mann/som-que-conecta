from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
from django.contrib.auth import get_user_model
from backend.accounts.serializers import UserRegistrationSerializer, UserProfileSerializer


User = get_user_model()

class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
