from rest_framework import serializers
from backend.articles.models import (
    Article,
    ArticleComments,
    ArticleFavorites
)
from backend.articles.validators import (
    validate_user_can_post_article,
)


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'


    def validate(self, data):
        validate_user_can_post_article(self.context['request'].user)
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
