from rest_framework import serializers
from backend.articles.models import (
    Article,
    ArticleComments,
    ArticleFavorites,
    ArticleCategory
)


class ArticleCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleCategory
        fields = ['id', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    # Campo para RECEBER o nome da categoria do frontend. Ele só existe na escrita.
    category_name = serializers.CharField(write_only=True, required=False)

    # Campo para MOSTRAR os dados da categoria na leitura. É apenas de leitura.
    category = ArticleCategorySerializer(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Article
        # Certifique-se de que o campo 'category' (de leitura) está na lista,
        # mas não o 'category_name' (que é apenas para escrita).
        # O DRF lida com isso automaticamente se o campo for write_only.
        fields = '__all__'

    def _get_category(self, category_name):
        """Método auxiliar para buscar a categoria ou lançar um erro."""
        try:
            return ArticleCategory.objects.get(name__iexact=category_name.strip())
        except ArticleCategory.DoesNotExist:
            raise serializers.ValidationError({
                'category': f"A categoria '{category_name}' não foi encontrada."
            })

    def create(self, validated_data):
        """
        Método chamado ao criar um novo artigo (POST).
        """
        # Pega o nome da categoria que veio do frontend
        category_name = validated_data.pop('category_name', None)
        if not category_name:
            raise serializers.ValidationError({'category': 'A categoria é obrigatória.'})

        # Busca o objeto da categoria correspondente
        category_obj = self._get_category(category_name)
        
        # Cria o artigo, associando o objeto de categoria encontrado
        article = Article.objects.create(category=category_obj, **validated_data)
        return article

    def update(self, instance, validated_data):
        """
        Método chamado ao atualizar um artigo (PATCH/PUT).
        """
        # Pega o nome da categoria, se ele foi enviado
        category_name = validated_data.pop('category_name', None)
        
        if category_name:
            # Se um novo nome de categoria foi enviado, busca o objeto e atualiza
            instance.category = self._get_category(category_name)
            
        # O super().update cuida da atualização dos outros campos
        return super().update(instance, validated_data)
    
    
class ArticleListSerializer(serializers.ModelSerializer):
    """
    Serializer otimizado para a lista de artigos.
    """
    # 1. Trocamos o CharField por um SerializerMethodField.
    #    Isso diz ao DRF para chamar o método get_author para obter o valor.
    author = serializers.SerializerMethodField()
    
    # Estes campos estão corretos
    category_name = serializers.CharField(write_only=True, required=False)

    # Campo para MOSTRAR os dados da categoria na leitura. É apenas de leitura.
    category = ArticleCategorySerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'short_description', 'cover_image', 'cover_link', 
            'reading_time', 'author', 'category', 'created_at', 'rating', 'read_count', 
            'is_published', 'comments_count', 'category_name'
        ]

    # 2. Corrigimos a lógica deste método.
    def get_author(self, obj):
        """
        Retorna um dicionário com os dados do autor (nome e foto)
        para ser consumido pelo frontend.
        """
        # Se por algum motivo o artigo não tiver autor, retorna null.
        if not obj.author:
            return None
            
        request = self.context.get('request')
        avatar_url = None
        
        # 3. Verificação e construção da URL corrigidas.
        #    Verifica se o campo 'profile_picture' existe e tem uma URL.
        if hasattr(obj.author, 'profile_picture') and obj.author.profile_picture and hasattr(obj.author.profile_picture, 'url'):
            avatar_url = request.build_absolute_uri(obj.author.profile_picture.url)

        # 4. Retorna um objeto com as chaves que o frontend espera.
        return {
            'name': obj.author.get_full_name() or obj.author.username,
            'avatar': avatar_url
        }



class ArticleCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user_id', read_only=True)

    class Meta:
        model = ArticleComments
        fields = '__all__'


class ArticleFavoriteSerializer(serializers.ModelSerializer):
    article = serializers.StringRelatedField(source='article_id', read_only=True)

    class Meta:
        model = ArticleFavorites
        fields = '__all__'
