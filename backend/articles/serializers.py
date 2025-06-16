from rest_framework import serializers
from backend.articles.models import (
    Article,
    ArticleComments,
    ArticleFavorites,
    ArticleCategory
)


class ArticleListSerializer(serializers.ModelSerializer):
    """
    Serializer otimizado para a lista de artigos.
    """
    # 1. Trocamos o CharField por um SerializerMethodField.
    #    Isso diz ao DRF para chamar o método get_author para obter o valor.
    author = serializers.SerializerMethodField()
    
    # Estes campos estão corretos
    category = serializers.CharField(source='category.name', read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'short_description', 'cover_image', 'cover_link', 
            'reading_time', 'author', 'category', 'created_at', 'rating', 'read_count', 
            'is_published', 'comments_count', 
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



class ArticleSerializer(serializers.ModelSerializer):
    # Serializer completo para detalhes, criação e edição
    author = serializers.StringRelatedField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Article
        fields = '__all__'



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


class ArticleCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ArticleCategory
        fields = '__all__'
