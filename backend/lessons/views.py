from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from backend.lessons.models import (
    Lesson,
)
from backend.lessons.serializers import (
    LessonSerializer,
)


class LessonsViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]