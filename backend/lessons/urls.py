from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.lessons.views import (
    LearningPathViewSet,
    LessonsViewSet,
    UserLearningProgressViewSet
)


router = DefaultRouter()
router.register('lessons', LessonsViewSet)
router.register('learningpath', LearningPathViewSet)
router.register('userlearningprogress', UserLearningProgressViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
