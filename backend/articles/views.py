from rest_framework.decorators import action, api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
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
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid
from backend.services.article_validation_service import article_validation_service
from rest_framework import status
from backend.articles.services import comment_validation_service
from rest_framework.exceptions import ValidationError


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

    @action(detail=True, methods=['post'])
    def submit_for_publication(self, request, pk=None):
        """
        Endpoint para submeter um artigo para publicação.
        O artigo deve estar em rascunho e ser do autor da requisição.
        O artigo passa por uma validação da IA antes de ser submetido.
        """
        article = self.get_object()
        
        # Verifica se o usuário é o autor do artigo
        if request.user != article.author:
            return Response(
                {'detail': 'Apenas o autor pode submeter o artigo para publicação.'},
                status=403
            )
        
        # Força o artigo para estado de rascunho antes de submeter
        article.is_draft = True
        article.is_published = False
        article.is_reviewed = False
        article.is_moderated = False
        article.save()
        
        # Valida o artigo usando a IA
        validation_result = article_validation_service.validate_article(article.content)
        
        if not validation_result['is_valid']:
            return Response({
                'detail': 'Erro na validação do artigo.',
                'error': validation_result['error']
            }, status=400)
            
        # Atualiza o artigo com o feedback da IA
        article.ai_feedback = validation_result['feedback']
        article.ai_bool = validation_result['is_approved']
        
        if not validation_result['is_approved']:
            article.is_draft = True
            article.is_published = False
            article.is_reviewed = False
            article.is_moderated = False
            article.save()
            return Response({
                'detail': 'O artigo não foi aprovado na revisão automática.',
                'feedback': validation_result['feedback'],
                'status': {
                    'is_draft': article.is_draft,
                    'is_published': article.is_published,
                    'is_reviewed': article.is_reviewed,
                    'is_moderated': article.is_moderated
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Se aprovado pela IA, atualiza o estado do artigo
        article.is_draft = False
        article.is_published = True
        article.is_reviewed = True
        article.is_moderated = True
        article.published_at = timezone.now()
        article.save()
        
        return Response({
            'detail': 'Artigo publicado com sucesso.',
            'feedback': validation_result['feedback'],
            'status': {
                'is_draft': article.is_draft,
                'is_published': article.is_published,
                'is_reviewed': article.is_reviewed,
                'is_moderated': article.is_moderated
            }
        })

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
        # Validação IA antes de salvar
        comment_text = request.data.get('comment')
        if not comment_text:
            return Response({'detail': 'O campo comment é obrigatório.'}, status=400)
        validation_result = comment_validation_service.validate_comment(comment_text)
        if not validation_result['is_valid']:
            return Response({
                'detail': 'Erro na validação do comentário.',
                'error': validation_result['error']
            }, status=400)
            
        # Se não foi aprovado pela IA, retorna o feedback sem salvar
        if not validation_result['is_approved']:
            return Response({
                'detail': 'Comentário não aprovado pela moderação.',
                'is_published': False,
                'ai_feedback': validation_result['feedback']
            }, status=200)
            
        # Só salva se passou pela IA e foi aprovado
        serializer = ArticleCommentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(
            article=article,
            user=request.user,
            is_published=True,
            is_moderated=True,
            ai_bool=True,
            ai_feedback=validation_result['feedback']
        )
        return Response(ArticleCommentSerializer(comment, context={'request': request}).data, status=201)

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
                'has_rated': False
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

    @action(detail=True, methods=['delete'])
    def remove_comment(self, request, pk=None):
        article = self.get_object()
        comment_id = request.data.get('comment_id')
        
        try:
            comment = ArticleComments.objects.get(
                id=comment_id,
                article=article
            )
            
            # Verifica se o usuário é o autor do comentário ou um administrador
            if not (request.user == comment.user or request.user.is_staff):
                return Response(
                    {'detail': 'Você não tem permissão para excluir este comentário.'},
                    status=403
                )
            
            comment.delete()
            return Response(status=204)
        except ArticleComments.DoesNotExist:
            return Response(
                {'detail': 'Comentário não encontrado.'},
                status=404
            )

    def destroy(self, request, *args, **kwargs):
        """
        Sobrescreve o método destroy para verificar permissões antes de excluir o artigo.
        Apenas o autor do artigo ou um administrador pode excluí-lo.
        """
        article = self.get_object()
        
        # Verifica se o usuário é o autor do artigo ou um administrador
        if not (request.user == article.author or request.user.is_staff):
            return Response(
                {'detail': 'Você não tem permissão para excluir este artigo.'},
                status=403
            )
        
        try:
            # Exclui o artigo
            self.perform_destroy(article)
            return Response(status=204)
        except Exception as e:
            return Response(
                {'detail': f'Erro ao excluir o artigo: {str(e)}'},
                status=500
            )

    def create(self, request, *args, **kwargs):
        """
        Cria um novo artigo e submete para validação da IA.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Valida o artigo usando a IA
        validation_result = article_validation_service.validate_article(serializer.validated_data['content'])
        
        if not validation_result['is_valid']:
            return Response({
                'detail': 'Erro na validação do artigo.',
                'error': validation_result['error']
            }, status=400)
            
        if not validation_result['is_approved']:
            # Salva o artigo como rascunho com o feedback da IA
            article = serializer.save(
                author=request.user,
                is_draft=True,
                is_published=False,
                is_reviewed=False,
                is_moderated=False,
                ai_feedback=validation_result['feedback'],
                ai_bool=validation_result['is_approved']
            )
            
            return Response({
                'detail': 'O artigo não foi aprovado na revisão automática.',
                'feedback': validation_result['feedback'],
                'status': {
                    'is_draft': article.is_draft,
                    'is_published': article.is_published,
                    'is_reviewed': article.is_reviewed,
                    'is_moderated': article.is_moderated
                }
            }, status=400)
        
        # Se aprovado pela IA, salva o artigo
        article = serializer.save(
            author=request.user,
            is_draft=False,
            is_published=False,
            is_reviewed=True,
            is_moderated=False,
            ai_feedback=validation_result['feedback'],
            ai_bool=validation_result['is_approved']
        )
        
        return Response({
            'detail': 'Artigo submetido para publicação com sucesso.',
            'feedback': validation_result['feedback'],
            'status': {
                'is_draft': article.is_draft,
                'is_published': article.is_published,
                'is_reviewed': article.is_reviewed,
                'is_moderated': article.is_moderated
            }
        }, status=201)

    def update(self, request, *args, **kwargs):
        """
        Atualiza um artigo existente e submete para validação da IA.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # Valida o artigo usando a IA
        validation_result = article_validation_service.validate_article(serializer.validated_data['content'])
        
        if not validation_result['is_valid']:
            return Response({
                'detail': 'Erro na validação do artigo.',
                'error': validation_result['error']
            }, status=400)
            
        if not validation_result['is_approved']:
            # Atualiza o artigo como rascunho com o feedback da IA
            article = serializer.save(
                is_draft=True,
                is_published=False,
                is_reviewed=False,
                is_moderated=False,
                ai_feedback=validation_result['feedback'],
                ai_bool=validation_result['is_approved']
            )
            
            return Response({
                'detail': 'O artigo não foi aprovado na revisão automática.',
                'feedback': validation_result['feedback'],
                'status': {
                    'is_draft': article.is_draft,
                    'is_published': article.is_published,
                    'is_reviewed': article.is_reviewed,
                    'is_moderated': article.is_moderated
                }
            }, status=400)
        
        # Se aprovado pela IA, atualiza o artigo
        article = serializer.save(
            is_draft=False,
            is_published=False,
            is_reviewed=True,
            is_moderated=False,
            ai_feedback=validation_result['feedback'],
            ai_bool=validation_result['is_approved']
        )
        
        return Response({
            'detail': 'Artigo submetido para publicação com sucesso.',
            'feedback': validation_result['feedback'],
            'status': {
                'is_draft': article.is_draft,
                'is_published': article.is_published,
                'is_reviewed': article.is_reviewed,
                'is_moderated': article.is_moderated
            }
        })


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def upload_article_image(request):
    """
    Endpoint para upload de imagens do editor de artigos.
    Retorna a URL da imagem para ser inserida no conteúdo.
    """
    if 'upload' not in request.FILES:
        return Response({'error': 'Nenhuma imagem enviada'}, status=400)
    
    image = request.FILES['upload']
    
    # Validação do tipo de arquivo
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp', 'image/tiff']
    if image.content_type not in allowed_types:
        return Response({'error': 'Tipo de arquivo não permitido'}, status=400)
    
    # Validação do tamanho (máximo 5MB)
    if image.size > 5 * 1024 * 1024:
        return Response({'error': 'Imagem muito grande. Máximo permitido: 5MB'}, status=400)
    
    try:
        # Gera um nome único para o arquivo
        ext = image.name.split('.')[-1]
        filename = f'articles_media/data/{uuid.uuid4()}.{ext}'
        
        # Salva o arquivo
        path = default_storage.save(filename, ContentFile(image.read()))
        
        # Gera a URL completa
        url = request.build_absolute_uri(default_storage.url(path))
        
        # Formato de resposta esperado pelo CKEditor
        return Response({
            'url': url,
            'uploaded': True,
            'fileName': filename,
            'error': None
        })
    except Exception as e:
        return Response({
            'uploaded': False,
            'error': {
                'message': f'Erro ao salvar a imagem: {str(e)}'
            }
        }, status=500)


class LatestArticleView(generics.ListAPIView):
    """
    Retorna apenas o último artigo publicado.
    Acesso público.
    """
    serializer_class = ArticleListSerializer
    permission_classes = [AllowAny] # Permite acesso sem autenticação

    def get_queryset(self):
        # Busca apenas artigos publicados, ordena pelo mais recente e pega só o primeiro
        return Article.objects.filter(is_published=True).order_by('-published_at')[:1]
