from django.db import models
from django.conf import settings


DIFICULTY = [
    ('BEGINNER', 'Iniciante'),
    ('INTERMEDIATE', 'Intermediário'),
    ('ADVANCED', 'Avançado'),
]


class ArticleCategory(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='Nome')
    
    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name='Título',
    )
    reading_time = models.IntegerField(
        null=False,
        blank=False,
        verbose_name='Tempo de leitura',
    )
    category = models.ForeignKey(
        ArticleCategory,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Categoria',
    )
    difficulty = models.CharField(
        choices=DIFICULTY,
        null=False,
        blank=False,
        verbose_name='Dificuldade',
    )
    read_count = models.IntegerField(
        null=False,
        blank=False,
        verbose_name='Quantidade de leituras',
        default=0,
    )
    like_count = models.IntegerField(
        null=False,
        blank=False,
        verbose_name='Quantidade de likes',
        default=0,
    )
    short_description = models.TextField(
        null=False,
        blank=False,
        verbose_name='Descrição curta',
    )
    cover_image = models.ImageField(
        upload_to='articles_media/cover/',
        default='articles_media/cover/default.png',
        blank=True,
        verbose_name='Imagem da capa do artigo',
    )
    cover_link = models.URLField(
        null=True,
        blank=True,
        verbose_name='Link da capa do artigo',
    )
    content = models.TextField(
        null=False,
        blank=False,
        verbose_name='Conteúdo',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Autor',
    )
    is_draft = models.BooleanField(
        default=True,
        verbose_name='Rascunho',
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Publicado',
    )
    is_reviewed = models.BooleanField(
        default=False,
        verbose_name='Revisado',
    )
    is_moderated = models.BooleanField(
        default=False,
        verbose_name='Moderado',
    )
    publishing_refused_reason = models.TextField(
        null=True,
        blank=True,
        verbose_name='Motivo de rejeição de publicação',
    )
    rating = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Avaliação',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em',
    )
    modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Modificado em',
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Publicado em',
    )

    def __str__(self):
        return f"{self.title} - {self.author.username}"

    class Meta:
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'


class ArticleComments(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Artigo',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuário',
    )
    comment = models.TextField(
        null=False,
        blank=False,
        verbose_name='Comentário',
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Publicado',
    )
    is_moderated = models.BooleanField(
        default=False,
        verbose_name='Moderado',
    )
    publishing_refused_reason = models.TextField(
        null=True,
        blank=True,
        verbose_name='Motivo de rejeição de publicação',
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em')
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name='Modificado em')

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Comentário de Artigo'
        verbose_name_plural = 'Comentários de Artigos'


class ArticleRating(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuário',
    )
    article_id = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Artigo',
    )
    rating = models.IntegerField(
        null=False,
        blank=False,
        verbose_name='Avaliação',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em',
    )

    class Meta:
        verbose_name = 'Avaliação de Artigo'
        verbose_name_plural = 'Avaliações de Artigos'
        
    def __str__(self):
        return f"{self.user.username} - {self.article.title} - {self.rating}"


class ArticleFavorites(models.Model):
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuário',
    )
    article_id = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Artigo',
    )
    
    def __str__(self):
        return f"{self.user.username} - {self.article.title}"
