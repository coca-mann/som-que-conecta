from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.articles.views import (
    TagViewSet,
    ArticleViewSet,
    ArticleCommentViewSet,
    ArticleFavoriteViewSet
)


router = DefaultRouter()
router.register('articles', ArticleViewSet)
router.register('articlecomments', ArticleCommentViewSet)
router.register('articlefavorites', ArticleFavoriteViewSet)
router.register('tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls))
]