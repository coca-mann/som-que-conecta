from rest_framework import serializers
from backend.articles.models import (
    Article,
    ArticleComments,
    ArticleFavorites,
    ArticleCategory
)
from backend.articles.validators import (
    validate_user_can_post_article,
)


class ArticleListSerializer(serializers.ModelSerializer):
    # Serializer mais "leve" apenas para a listagem
    author = serializers.CharField(source='author.username', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'short_description', 'cover_image', 'cover_link', 
            'reading_time', 'author', 'category', 'created_at', 'rating'
        ]


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
