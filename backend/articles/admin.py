from django.contrib import admin
from .models import Article, ArticleComments, ArticleRating, ArticleFavorites



admin.site.register(ArticleComments)
admin.site.register(ArticleRating)
admin.site.register(ArticleFavorites)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
