from rest_framework import serializers
from django.contrib.auth import get_user_model
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


class ArticleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        # Garanta que seu modelo de usuário tenha um campo para foto de perfil
        fields = ['id', 'username', 'get_full_name','first_name', 'last_name', 'profile_picture']

class ArticleCommentSerializer(serializers.ModelSerializer):
    # Use o serializer de autor aninhado aqui
    user = ArticleAuthorSerializer(read_only=True)

    class Meta:
        model = ArticleComments
        fields = ['id', 'user', 'comment', 'created_at']


class ArticleSerializer(serializers.ModelSerializer):
    # Campo para RECEBER o nome da categoria do frontend. Ele só existe na escrita.
    category_name = serializers.CharField(write_only=True, required=False)

    # Campo para MOSTRAR os dados da categoria na leitura. É apenas de leitura.
    category = ArticleCategorySerializer(read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    comments = ArticleCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        # Certifique-se de que o campo 'category' (de leitura) está na lista,
        # mas não o 'category_name' (que é apenas para escrita).
        # O DRF lida com isso automaticamente se o campo for write_only.
        fields = [
            'id', 'title', 'reading_time', 'category', 'difficulty', 'read_count',
            'like_count', 'short_description', 'cover_image', 'cover_link',
            'content', 'author', 'is_published', 'created_at', 'comments'
        ]

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
    author = ArticleAuthorSerializer(read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'short_description', 'cover_image', 'cover_link', 'reading_time',
            'author', 'category', 'created_at', 'rating', 'read_count', 'is_published', 'comments_count'
        ]
        
        
class ArticleDetailSerializer(serializers.ModelSerializer):
    author = ArticleAuthorSerializer(read_only=True)
    category = ArticleCategorySerializer(read_only=True)
    comments = ArticleCommentSerializer(many=True, read_only=True)
    cover_image = serializers.SerializerMethodField()
    favorite_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'short_description', 'content', 'cover_image', 'cover_link',
            'reading_time', 'difficulty', 'author', 'category', 'comments', 'created_at',
            'read_count', 'like_count', 'rating', 'is_published', 'favorite_count'
        ]

    def get_cover_image(self, obj):
        request = self.context.get('request')
        if obj.cover_image:
            return request.build_absolute_uri(obj.cover_image.url) if request else obj.cover_image.url
        return obj.cover_link

    def get_favorite_count(self, obj):
        return ArticleFavorites.objects.filter(article_id=obj).count()


# --- Serializer para CRIAR e ATUALIZAR um Artigo (ações 'create', 'update', 'partial_update') ---
class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    # Recebe o ID da categoria, que é o que o formulário Vue envia
    category_name = serializers.CharField(write_only=True, required=False)

    # Campo para MOSTRAR os dados da categoria na leitura. É apenas de leitura.
    category = ArticleCategorySerializer(read_only=True)

    class Meta:
        model = Article
        # Lista de campos que o frontend pode enviar ao criar/editar
        fields = [
            'title', 'short_description', 'content', 'cover_image', 'cover_link',
            'reading_time', 'difficulty', 'category', 'is_draft', 'is_published', 'category_name'
        ]

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


class ArticleFavoriteSerializer(serializers.ModelSerializer):
    article = serializers.StringRelatedField(source='article_id', read_only=True)

    class Meta:
        model = ArticleFavorites
        fields = '__all__'
