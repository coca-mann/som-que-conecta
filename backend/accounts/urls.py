from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import UserRegistrationViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='register')
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]
