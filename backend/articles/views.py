from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from backend.articles.models import (
    Tag,
    ArticleFavorites,
    Article,
    ArticleComments
)
from backend.articles.serializers import (
    TagSerializer,
    ArticleSerializer,
    ArticleFavoriteSerializer,
    ArticleCommentSerializer
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated]


class ArticleCommentViewSet(viewsets.ModelViewSet):
    queryset = ArticleComments.objects.all()
    serializer_class = ArticleCommentSerializer
    permission_classes = [IsAuthenticated]


class ArticleFavoriteViewSet(viewsets.ModelViewSet):
    queryset = ArticleFavorites.objects.all()
    serializer_class = ArticleFavoriteSerializer
    permission_classes = [IsAuthenticated]
