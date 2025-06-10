from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserRegistrationViewSet, UserDetailView

router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserDetailView.as_view(), name='user-detail'),
]
