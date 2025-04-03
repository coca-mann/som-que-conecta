from rest_framework.routers import DefaultRouter
from django.urls import path, include
from backend.notifications.views import NotificationsViewSet


router = DefaultRouter()
router.register('notifications', NotificationsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
