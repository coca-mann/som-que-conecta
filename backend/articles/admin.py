from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Avg
from .models import (
    Article, 
    ArticleComments, 
    ArticleRating, 
    ArticleFavorites, 
    ArticleCategory,
    ArticleRead
)


@admin.register(ArticleCategory)
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'article_count')
    search_fields = ('name',)
    ordering = ('name',)
    
    def article_count(self, obj):
        return obj.article_set.count()
    article_count.short_description = 'Quantidade de Artigos'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'author', 
        'category', 
        'difficulty', 
        'status_display',
        'read_count', 
        'like_count',
        'rating_display',
        'created_at'
    )
    list_filter = (
        'category',
        'difficulty',
        'is_draft',
        'is_published',
        'is_reviewed',
        'is_moderated',
        'ai_bool',
        'created_at',
        'published_at',
    )
    search_fields = ('title', 'short_description', 'content', 'author__username', 'author__email')
    readonly_fields = ('read_count', 'like_count', 'created_at', 'modified_at')
    prepopulated_fields = {'title': ('short_description',)}
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('title', 'short_description', 'content', 'author', 'category', 'difficulty', 'reading_time')
        }),
        ('Mídia', {
            'fields': ('cover_image', 'cover_link'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_draft', 'is_published', 'is_reviewed', 'is_moderated'),
            'classes': ('collapse',)
        }),
        ('IA e Avaliação', {
            'fields': ('ai_bool', 'ai_feedback', 'rating'),
            'classes': ('collapse',)
        }),
        ('Estatísticas', {
            'fields': ('read_count', 'like_count'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('created_at', 'modified_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['publish_articles', 'unpublish_articles', 'mark_as_reviewed', 'mark_as_moderated']
    
    def status_display(self, obj):
        if obj.is_published:
            return format_html('<span style="color: green;">✓ Publicado</span>')
        elif obj.is_draft:
            return format_html('<span style="color: orange;">📝 Rascunho</span>')
        else:
            return format_html('<span style="color: red;">❌ Não publicado</span>')
    status_display.short_description = 'Status'
    
    def rating_display(self, obj):
        if obj.rating:
            stars = '★' * obj.rating + '☆' * (5 - obj.rating)
            return format_html('<span style="color: gold;">{}</span>', stars)
        return '-'
    rating_display.short_description = 'Avaliação'
    
    def publish_articles(self, request, queryset):
        updated = queryset.update(is_published=True, is_draft=False)
        self.message_user(request, f'{updated} artigos foram publicados com sucesso.')
    publish_articles.short_description = "Publicar artigos selecionados"
    
    def unpublish_articles(self, request, queryset):
        updated = queryset.update(is_published=False, is_draft=True)
        self.message_user(request, f'{updated} artigos foram despublicados com sucesso.')
    unpublish_articles.short_description = "Despublicar artigos selecionados"
    
    def mark_as_reviewed(self, request, queryset):
        updated = queryset.update(is_reviewed=True)
        self.message_user(request, f'{updated} artigos foram marcados como revisados.')
    mark_as_reviewed.short_description = "Marcar como revisado"
    
    def mark_as_moderated(self, request, queryset):
        updated = queryset.update(is_moderated=True)
        self.message_user(request, f'{updated} artigos foram marcados como moderados.')
    mark_as_moderated.short_description = "Marcar como moderado"


@admin.register(ArticleComments)
class ArticleCommentsAdmin(admin.ModelAdmin):
    list_display = ('comment_preview', 'article', 'user', 'status_display', 'ai_feedback_display', 'created_at')
    list_filter = ('is_published', 'is_moderated', 'ai_bool', 'created_at')
    search_fields = ('comment', 'article__title', 'user__username', 'user__email')
    readonly_fields = ('created_at', 'modified_at')
    list_per_page = 25
    
    fieldsets = (
        ('Comentário', {
            'fields': ('article', 'user', 'comment')
        }),
        ('Status', {
            'fields': ('is_published', 'is_moderated')
        }),
        ('IA', {
            'fields': ('ai_bool', 'ai_feedback'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('created_at', 'modified_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_comments', 'reject_comments', 'mark_as_moderated']
    
    def comment_preview(self, obj):
        return obj.comment[:100] + '...' if len(obj.comment) > 100 else obj.comment
    comment_preview.short_description = 'Comentário'
    
    def status_display(self, obj):
        if obj.is_published:
            return format_html('<span style="color: green;">✓ Aprovado</span>')
        else:
            return format_html('<span style="color: red;">❌ Pendente</span>')
    status_display.short_description = 'Status'
    
    def ai_feedback_display(self, obj):
        if obj.ai_bool is True:
            return format_html('<span style="color: green;">✓ Aprovado pela IA</span>')
        elif obj.ai_bool is False:
            return format_html('<span style="color: red;">❌ Rejeitado pela IA</span>')
        return '-'
    ai_feedback_display.short_description = 'IA'
    
    def approve_comments(self, request, queryset):
        updated = queryset.update(is_published=True, is_moderated=True)
        self.message_user(request, f'{updated} comentários foram aprovados.')
    approve_comments.short_description = "Aprovar comentários selecionados"
    
    def reject_comments(self, request, queryset):
        updated = queryset.update(is_published=False, is_moderated=True)
        self.message_user(request, f'{updated} comentários foram rejeitados.')
    reject_comments.short_description = "Rejeitar comentários selecionados"
    
    def mark_as_moderated(self, request, queryset):
        updated = queryset.update(is_moderated=True)
        self.message_user(request, f'{updated} comentários foram marcados como moderados.')
    mark_as_moderated.short_description = "Marcar como moderado"


@admin.register(ArticleRating)
class ArticleRatingAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'article_id', 'rating_stars', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user_id__username', 'user_id__email', 'article_id__title')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    def rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html('<span style="color: gold;">{}</span>', stars)
    rating_stars.short_description = 'Avaliação'


@admin.register(ArticleFavorites)
class ArticleFavoritesAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'article_id')
    search_fields = ('user_id__username', 'user_id__email', 'article_id__title')
    list_per_page = 25


@admin.register(ArticleRead)
class ArticleReadAdmin(admin.ModelAdmin):
    list_display = ('article', 'user', 'ip_address', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('article__title', 'user__username', 'user__email', 'ip_address')
    readonly_fields = ('created_at',)
    list_per_page = 25
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('article', 'user')
