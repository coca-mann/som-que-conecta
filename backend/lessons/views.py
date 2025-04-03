from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from backend.lessons.models import (
    Lessons,
    LearningPaths,
    UserLearningProgress
)
from backend.lessons.serializers import (
    LearningPathSerializer,
    LessonSerializer,
    UserLearningProgressSerializer
)


class LessonsViewSet(viewsets.ModelViewSet):
    queryset = Lessons.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LearningPathViewSet(viewsets.ModelViewSet):
    queryset = LearningPaths.objects.all()
    serializer_class = LearningPathSerializer
    permission_classes = [IsAuthenticated]


class UserLearningProgressViewSet(viewsets.ModelViewSet):
    queryset = UserLearningProgress.objects.all()
    serializer_class = UserLearningProgressSerializer
    permission_classes = [IsAuthenticated]
