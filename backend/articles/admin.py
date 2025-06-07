from django.contrib import admin
from .models import Article, ArticleComments, ArticleRating, ArticleFavorites



admin.site.register(ArticleComments)
admin.site.register(ArticleRating)
admin.site.register(ArticleFavorites)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_tags', 'created_at')

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = "Tags"
