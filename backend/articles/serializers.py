from rest_framework import serializers
from backend.articles.models import (
    Tag,
    Article,
    ArticleComments,
    ArticleFavorites
)
from backend.articles.validators import (
    validate_user_can_post_article,
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = '__all__'


    def validate(self, data):
        user = self.context['request'].user
        validate_user_can_post_article(user)
        return data


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
