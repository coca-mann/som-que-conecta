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

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_staff:
            return Article.objects.all()
        return Article.objects.filter(is_published=True)


class ArticleCommentViewSet(viewsets.ModelViewSet):
    queryset = ArticleComments.objects.all()
    serializer_class = ArticleCommentSerializer
    permission_classes = [IsAuthenticated]


class ArticleFavoriteViewSet(viewsets.ModelViewSet):
    queryset = ArticleFavorites.objects.all()
    serializer_class = ArticleFavoriteSerializer
    permission_classes = [IsAuthenticated]
