from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.lessons.views import (
    LessonsViewSet, 
    TaskActionViewSet, 
    UserTaskViewSet,
    SkillLevelsView,
    InstrumentTypesView,
    TaskAditionalResourceViewSet,
    LatestLessonView
)


router = DefaultRouter()
router.register(r'lessons', LessonsViewSet, basename='lesson')
router.register(r'tasks', TaskActionViewSet, basename='task-action')
router.register(r'user-tasks', UserTaskViewSet, basename='user-task')
router.register(r'task-resources', TaskAditionalResourceViewSet, basename='task-resources')

urlpatterns = [
    path('skill-levels/', SkillLevelsView.as_view(), name='skill-levels'),
    path('instrument-types/', InstrumentTypesView.as_view(), name='instrument-types'),
    path('lessons/latest/', LatestLessonView.as_view(), name='latest-lesson'),
    path('', include(router.urls)),
]
