from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.articles.views import (
    ArticleViewSet,
    ArticleCommentViewSet,
    ArticleFavoriteViewSet,
    ArticleCategoryViewSet
)


router = DefaultRouter()
router.register('articles', ArticleViewSet, basename='articles')
router.register('articlecomments', ArticleCommentViewSet)
router.register('articlefavorites', ArticleFavoriteViewSet)
router.register('article-categories', ArticleCategoryViewSet)

urlpatterns = [
    path('', include(router.urls))
]
