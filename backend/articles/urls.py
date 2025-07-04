from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend.articles.views import (
    ArticleViewSet,
    ArticleFavoriteViewSet,
    ArticleCategoryViewSet,
    upload_article_image,
    LatestArticleView
)


router = DefaultRouter()
router.register('articles', ArticleViewSet, basename='articles')
router.register('articlefavorites', ArticleFavoriteViewSet)
router.register('article-categories', ArticleCategoryViewSet)

urlpatterns = [
    path('articles/upload-image/', upload_article_image, name='article-upload-image'),
    path('articles/latest/', LatestArticleView.as_view(), name='latest-article'),
    path('', include(router.urls)),
]
