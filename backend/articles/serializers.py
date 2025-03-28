from rest_framework import serializers
from .models import Tag, Article, ArticleComments, ArticleFavorites
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)


    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'content',
            'author',
            'tags',
            'is_published',
            'created_at',
            'modified_at',
        ]


class ArticleCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user_id', read_only=True)


    class Meta:
        model = ArticleComments
        fields = [
            'id',
            'article_id',
            'user',
            'content',
            'created_at',
            'modified_at',
        ]


class ArticleFavoriteSerializer(serializers.ModelSerializer):
    article = serializers.StringRelatedField(source='article_id', read_only=True)


    class Meta:
        model = ArticleFavorites
        fields = [
            'id',
            'user_id',
            'article',
            'created_at',
        ]