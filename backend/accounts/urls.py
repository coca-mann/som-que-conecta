from django.urls import path
from .views import (
    UserRegistrationView,
    UserProfileView,
    PublicUserProfileView,
    UpdateUserProfileView)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/<str:username>', PublicUserProfileView.as_view(), name='user-by-username'),
    path('update/', UpdateUserProfileView.as_view(), name='update-user-profile'),
]