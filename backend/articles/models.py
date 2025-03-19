from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nome da Tag')

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='Título')
    content = models.JSONField(verbose_name='Conteúdo do Artigo')
    author = models.CharField(max_length=255, null=True, blank=True, verbose_name='Autor')
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True, verbose_name='Tags')
    is_published = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title}"

class ArticleComments(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class ArticleFavorites(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    article_id = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)