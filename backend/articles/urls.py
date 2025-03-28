from django.urls import path
from .views import (
    TagView,
    ArticleDetailView,
    ArticleListCreateView, 
    ArticleCommentListCreateView,
    ArticleFavoriteListCreateView
)


urlpatterns = [
    path('tags/', TagView.as_view(), name='tag-list'),
    path('articles/', ArticleListCreateView.as_view(), name='article-list-create'),
    path('articles/<int:pk>', ArticleDetailView.as_view(), name='article-detail'),
    path('comments/', ArticleCommentListCreateView.as_view(), name='comment-list-create'),
    path('favorites/', ArticleFavoriteListCreateView.as_view(), name='favorites-list-create'),
]