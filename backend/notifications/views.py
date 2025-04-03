from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from backend.notifications.serializers import NotificationSerializer
from backend.notifications.models import Notifications


class NotificationsViewSet(viewsets.ModelViewSet):
    queryset = Notifications.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
