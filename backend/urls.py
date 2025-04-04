from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from backend.accounts.views_social import GoogleLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('backend.instruments.urls')),
    path('api/v1/', include('backend.lessons.urls')),
    path('api/v1/', include('backend.articles.urls')),
    path('api/v1/', include('backend.accounts.urls')),
    path('api/v1/', include('backend.notifications.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/social/', include('allauth.socialaccount.urls')),
    path('auth/social/login/', GoogleLogin.as_view(), name='google-login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
