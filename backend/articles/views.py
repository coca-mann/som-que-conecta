from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Tag, ArticleFavorites, Article, ArticleComments
from .serializers import (
    TagSerializer,
    ArticleSerializer,
    ArticleFavoriteSerializer,
    ArticleCommentSerializer
)
from django.shortcuts import get_object_or_404


class TagView(APIView):
    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    

class ArticleListCreateView(APIView):
    def get(self, request):
        articles = Article.objects.all().order_by('-created_at')
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ArticleDetailView(APIView):
    def get(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)
    

class ArticleCommentListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        comments = ArticleComments.objects.all().order_by('-created_at')
        serializer = ArticleCommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data.copy()
        data['user_id'] = request.user.id
        serializer = ArticleCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ArticleFavoriteListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        favorites = ArticleFavorites.objects.filter(user_id=request.user)
        serializer = ArticleFavoriteSerializer(favorites, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data.copy()
        data['user_id'] = request.user.id
        serializer = ArticleFavoriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
