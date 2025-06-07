from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.articles.views import (
    ArticleViewSet,
    ArticleCommentViewSet,
    ArticleFavoriteViewSet
)


router = DefaultRouter()
router.register('articles', ArticleViewSet)
router.register('articlecomments', ArticleCommentViewSet)
router.register('articlefavorites', ArticleFavoriteViewSet)

urlpatterns = [
    path('', include(router.urls))
]
