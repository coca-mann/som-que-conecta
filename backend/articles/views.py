from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from backend.articles.models import (
    ArticleFavorites,
    Article,
    ArticleComments,
    ArticleCategory
)
from backend.articles.serializers import (
    ArticleSerializer,
    ArticleFavoriteSerializer,
    ArticleCommentSerializer,
    ArticleCategorySerializer,
    ArticleListSerializer
)
from backend.articles.permissions import IsCommentAuthorOrAdmin


class ArticleCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArticleCategory.objects.all()
    serializer_class = ArticleCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    # serializer_class = ArticleSerializer # Remova o atributo de classe
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        """
        Retorna um serializer diferente para a ação 'list' (mais leve)
        e outro para as demais ações como 'retrieve', 'create', etc. (completo).
        """
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleSerializer # Serializer padrão para as outras ações

    def get_queryset(self):
        # Sua lógica de queryset continua a mesma
        user = self.request.user
        queryset = Article.objects.all() if user.is_authenticated and user.is_staff else Article.objects.filter(is_published=True)
        # ... resto da sua lógica de filtro ...
        return queryset

    def perform_create(self, serializer):
        # Sua lógica de perform_create continua a mesma
        serializer.save(author=self.request.user)



class ArticleCommentViewSet(viewsets.ModelViewSet):
    queryset = ArticleComments.objects.all()
    serializer_class = ArticleCommentSerializer
    permission_classes = [IsCommentAuthorOrAdmin, IsAuthenticated]


    def perform_create(self, serializer):
        user = self.request.user
        serializer = serializer.save(user_id=user)


class ArticleFavoriteViewSet(GenericViewSet):
    queryset = ArticleFavorites.objects.all()
    serializer_class = ArticleFavoriteSerializer
    permission_classes = [IsAuthenticated]


    @action(detail=False, methods=['get', 'post', 'delete'], url_path='favorite')
    def favorite(self, request):
        user = request.user
        article_id = request.query_params.get("article_id")
        if not article_id:
            return Response({'detail': 'Parâmetro article_id é obrigatório.'}, status=400)

        article = Article.objects.filter(pk=article_id).first()
        if not article:
            return Response({'detail': 'Artigo não encontrado'}, status=404)

        if request.method == 'POST':
            favorite, created = ArticleFavorites.objects.get_or_create(user_id=user, article_id=article)
            if not created:
                return Response({'detail': 'Artigo já está favoritado'}, status=200)
            return Response({'detail': 'Artigo favoritado com sucesso'}, status=201)

        elif request.method == 'DELETE':
            favorite = ArticleFavorites.objects.filter(user_id=user, article_id=article).first()
            if not favorite:
                return Response({'detail': 'Favorito não encontrado'}, status=404)
            favorite.delete()
            return Response({'detail': 'Artigo desfavoritado com sucesso'}, status=204)

        elif request.method == 'GET':
            favorited = ArticleFavorites.objects.filter(user_id=user, article_id=article).exists()
            return Response({'favorited': favorited})

        return Response({'detail': 'Método não permitido'}, status=405)
