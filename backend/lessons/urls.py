from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.lessons.views import (
    LessonsViewSet,
)


router = DefaultRouter()
router.register('lessons', LessonsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
