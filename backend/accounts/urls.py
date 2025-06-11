from rest_framework.routers import DefaultRouter
from django.urls import path, include
from backend.accounts.views import UserRegistrationViewSet, UserDetailView, ProfileView, InProgressCourseListView, RecentActivityListView
from backend.instruments.views import UserInstrumentListView

router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='register')

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('profile/', ProfileView.as_view(), name='user-profile'),
    path('profile/in-progress-courses/', InProgressCourseListView.as_view(), name='in-progress-courses'),
    path('profile/my-instruments/', UserInstrumentListView.as_view(), name='my-instruments'),
    path('profile/recent-activity/', RecentActivityListView.as_view(), name='recent-activity'),
]
