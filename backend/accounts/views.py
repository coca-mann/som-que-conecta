from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoModelPermissions
from django.contrib.auth.models import User
from backend.accounts.serializers import UserRegistrationSerializer, UserProfileSerializer
from backend.accounts.models import UserProfile


class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserProfileViewSet(viewsets.GenericViewSet,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)