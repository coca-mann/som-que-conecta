from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.lessons.views import (
    LessonsViewSet, 
    TaskActionViewSet, 
    UserTaskViewSet,
    SkillLevelsView,
    InstrumentTypesView
)


router = DefaultRouter()
router.register(r'lessons', LessonsViewSet, basename='lesson')
router.register(r'tasks', TaskActionViewSet, basename='task-action')
router.register(r'user-tasks', UserTaskViewSet, basename='user-task')

urlpatterns = [
    path('', include(router.urls)),
    path('skill-levels/', SkillLevelsView.as_view(), name='skill-levels'),
    path('instrument-types/', InstrumentTypesView.as_view(), name='instrument-types'),
]
