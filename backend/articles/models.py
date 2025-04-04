from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nome da Tag')

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='Título')
    content = CKEditor5Field('Conteudo', config_name='extends')
    author = models.CharField(max_length=255, null=True, blank=True, verbose_name='Autor')
    tags = models.ManyToManyField(Tag, related_name='articles', blank=True, verbose_name='Tags')
    is_published = models.BooleanField(verbose_name='Publicado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modificado em')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'


class ArticleComments(models.Model):
    article_id = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, verbose_name='Artigo')
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Usuário')
    content = models.TextField(blank=False, verbose_name='Conteúdo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='Modificado em')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Comentário de Artigo'
        verbose_name_plural = 'Comentários de Artigos'


class ArticleFavorites(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Usuário')
    article_id = models.ForeignKey(Article, on_delete=models.SET_NULL, null=True, verbose_name='Artigo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    class Meta:
        verbose_name = 'Artigo Favorito'
        verbose_name_plural = 'Artigos Favoritos'
