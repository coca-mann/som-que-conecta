from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.filters import OrderingFilter
from django.db.models import F, Q, Count, Avg
from backend.articles.models import (
    ArticleFavorites,
    Article,
    ArticleComments,
    ArticleCategory,
    ArticleRating,
    ArticleRead
)
from backend.articles.serializers import (
    ArticleSerializer,
    ArticleFavoriteSerializer,
    ArticleCommentSerializer,
    ArticleCategorySerializer,
    ArticleListSerializer,
    ArticleDetailSerializer,
    ArticleCreateUpdateSerializer
)
from backend.articles.permissions import IsCommentAuthorOrAdmin
from django.utils import timezone
from datetime import timedelta


class ArticleCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArticleCategory.objects.all()
    serializer_class = ArticleCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArticleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Artigos com a lógica de filtro e ordenação corrigida.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'read_count', 'rating']
    ordering = ['-created_at']

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def register_read(self, article, request):
        """
        Registra uma leitura do artigo, usando o tempo de leitura do artigo como intervalo.
        """
        now = timezone.now()
        ip_address = self.get_client_ip(request)
        
        # Converte o tempo de leitura (em minutos) para timedelta
        reading_interval = timedelta(minutes=article.reading_time)
        
        # Verifica se já houve uma leitura recente (baseado no tempo de leitura do artigo)
        recent_read = ArticleRead.objects.filter(
            article=article,
            created_at__gte=now - reading_interval
        )
        
        if request.user.is_authenticated:
            recent_read = recent_read.filter(user=request.user)
        else:
            recent_read = recent_read.filter(ip_address=ip_address)
        
        if not recent_read.exists():
            # Registra a nova leitura
            ArticleRead.objects.create(
                article=article,
                user=request.user if request.user.is_authenticated else None,
                ip_address=ip_address if not request.user.is_authenticated else None
            )
            
            # Atualiza o contador do artigo
            article.read_count = ArticleRead.objects.filter(article=article).count()
            article.save()

    def retrieve(self, request, *args, **kwargs):
        """
        Sobrescreve o método retrieve para registrar a leitura.
        """
        instance = self.get_object()
        self.register_read(instance, request)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_class(self):
        """
        Retorna o serializer correto para cada ação.
        """
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ArticleCreateUpdateSerializer
        elif self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        """
        Constrói o queryset na ordem correta:
        1. Filtra por publicação (a regra de negócio principal).
        2. Aplica filtros de query (categoria, busca).
        3. Anota para permitir ordenação por popularidade.
        """
        user = self.request.user

        # PASSO 1: Define o queryset base com a regra de publicação.
        if user.is_authenticated and user.is_staff:
            base_queryset = Article.objects.all()
        else:
            base_queryset = Article.objects.filter(is_published=True)
        
        # PASSO 2: Aplica os filtros da URL sobre o queryset base.
        category_param = self.request.query_params.get("category")
        if category_param:
            base_queryset = base_queryset.filter(category__name__iexact=category_param)

        search_param = self.request.query_params.get("search")
        if search_param:
            base_queryset = base_queryset.filter(
                Q(title__icontains=search_param) | 
                Q(short_description__icontains=search_param)
            )
        
        # PASSO 3: Aplica a anotação para ordenação.
        # Isso deve ser feito após os filtros para otimização.
        final_queryset = base_queryset.annotate(
            popularity=F('like_count') + F('read_count'),
            comments_count=Count('articlecomments'),
            avg_rating=Avg('rating')
        )
            
        return final_queryset

    def perform_create(self, serializer):
        """ Associa o artigo ao usuário logado ao criar. """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def check_favorite(self, request, pk=None):
        article = self.get_object()
        is_favorited = ArticleFavorites.objects.filter(
            user_id=request.user,
            article_id=article
        ).exists()
        return Response({'is_favorited': is_favorited})

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        article = self.get_object()
        favorite, created = ArticleFavorites.objects.get_or_create(
            user_id=request.user,
            article_id=article
        )
        if not created:
            return Response({'detail': 'Artigo já está nos favoritos'}, status=400)
        return Response({'detail': 'Artigo adicionado aos favoritos'}, status=201)

    @action(detail=True, methods=['delete'])
    def unfavorite(self, request, pk=None):
        article = self.get_object()
        try:
            favorite = ArticleFavorites.objects.get(
                user_id=request.user,
                article_id=article
            )
            favorite.delete()
            return Response(status=204)
        except ArticleFavorites.DoesNotExist:
            return Response({'detail': 'Artigo não está nos favoritos'}, status=404)

    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        article = self.get_object()
        serializer = ArticleCommentSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save(
                article=article,
                user=request.user,
                is_published=True  # Você pode ajustar isso baseado na sua lógica de moderação
            )
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        article = self.get_object()
        comments = ArticleComments.objects.filter(
            article=article,
            is_published=True
        ).order_by('-created_at')
        
        serializer = ArticleCommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        article = self.get_object()
        rating_value = request.data.get('rating')
        
        if not rating_value or not isinstance(rating_value, int) or rating_value < 1 or rating_value > 5:
            return Response({'detail': 'Avaliação inválida. Deve ser um número entre 1 e 5.'}, status=400)
        
        # Atualiza ou cria a avaliação
        rating, created = ArticleRating.objects.update_or_create(
            user_id=request.user,
            article_id=article,
            defaults={'rating': rating_value}
        )
        
        # Calcula a média das avaliações
        ratings = ArticleRating.objects.filter(article_id=article)
        avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
        
        # Atualiza a avaliação média no artigo
        article.rating = round(avg_rating, 1) if avg_rating else None
        article.save()
        
        return Response({
            'detail': 'Avaliação registrada com sucesso',
            'rating': article.rating
        })

    @action(detail=True, methods=['get'])
    def check_rating(self, request, pk=None):
        article = self.get_object()
        try:
            rating = ArticleRating.objects.get(
                user_id=request.user,
                article_id=article
            )
            return Response({
                'has_rated': True,
                'rating': rating.rating
            })
        except ArticleRating.DoesNotExist:
            return Response({
                'has_rated': False,
                'rating': None
            })

    @action(detail=True, methods=['delete'])
    def remove_rating(self, request, pk=None):
        article = self.get_object()
        try:
            rating = ArticleRating.objects.get(
                user_id=request.user,
                article_id=article
            )
            rating.delete()
            
            # Recalcula a média das avaliações
            ratings = ArticleRating.objects.filter(article_id=article)
            avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
            
            # Atualiza a avaliação média no artigo
            article.rating = round(avg_rating, 1) if avg_rating else None
            article.save()
            
            return Response({
                'detail': 'Avaliação removida com sucesso',
                'rating': article.rating
            })
        except ArticleRating.DoesNotExist:
            return Response({
                'detail': 'Você ainda não avaliou este artigo'
            }, status=404)


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
