<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Back Navigation -->
    <div class="mb-6">
      <button @click="goBack" class="flex items-center gap-2 text-blue-600 hover:text-blue-800 transition-colors">
        <ArrowLeft class="h-4 w-4" />
        Voltar aos Artigos
      </button>
    </div>

    <div v-if="article" class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Article Header -->
      <article class="bg-white rounded-lg shadow-lg overflow-hidden">
        <div class="relative h-64 md:h-80">
          <div class="absolute inset-0">
            <img :src="article.cover_image" :alt="article.title" class="w-full h-full object-cover">
          </div>
          <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end">
            <div class="p-6 text-white">
              <div class="flex items-center gap-3 mb-3">
                <span class="px-3 py-1 bg-blue-600 rounded-full text-sm font-medium">
                  {{ article.category?.name || article.category }}
                </span>
                <span class="text-sm opacity-90">{{ formatDate(article.created_at) }}</span>
              </div>
              <h1 class="text-3xl md:text-4xl font-bold leading-tight">{{ article.title }}</h1>
            </div>
          </div>
        </div>

        <!-- Article Meta -->
        <div class="p-6 border-b border-gray-200">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div class="flex items-center gap-4">
              <img :src="article.author.profile_picture" :alt="article.author.get_full_name" class="w-12 h-12 rounded-full">
              <div>
                <h3 class="font-semibold text-gray-900">{{ article.author.get_full_name }}</h3>
              </div>
            </div>
            
            <div class="flex items-center gap-6">
              <div class="flex items-center gap-2">
                <Clock class="h-4 w-4 text-gray-500" />
                <span class="text-sm text-gray-600">{{ article.reading_time }} min de leitura</span>
              </div>
              
              <div class="flex items-center gap-2">
                <Eye class="h-4 w-4 text-gray-500" />
                <span class="text-sm text-gray-600">{{ article.read_count }} visualizações</span>
              </div>
              
              <div class="flex items-center gap-1">
                <Star v-for="star in 5" :key="star" 
                     :class="star <= Math.floor(article.rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'"
                     class="h-4 w-4" />
                <span class="text-sm text-gray-600 ml-1">({{ article.rating }})</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Article Content -->
        <div class="p-6 md:p-8">
          <div class="prose prose-lg max-w-none">
            <p class="text-xl text-gray-600 mb-6 font-medium">{{ article.excerpt }}</p>
            
            <div v-html="article.content" class="space-y-6 [&>h2]:text-2xl [&>h2]:font-bold [&>h2]:text-gray-900 [&>h2]:mt-8 [&>h2]:mb-4 [&>h3]:text-xl [&>h3]:font-semibold [&>h3]:text-gray-900 [&>h3]:mt-6 [&>h3]:mb-3 [&>p]:text-gray-700 [&>p]:leading-relaxed [&>p]:mb-4 [&>ul]:list-disc [&>ul]:list-inside [&>ul]:space-y-2 [&>ul]:mb-4 [&>ul]:text-gray-700 [&>li]:ml-4 [&>strong]:font-semibold [&>strong]:text-gray-900"></div>
          </div>
        </div>

        <!-- Article Actions -->
        <div class="p-6 bg-gray-50 border-t border-gray-200">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <button @click="toggleLike" :class="[
                'flex items-center gap-2 px-4 py-2 rounded-lg transition-colors',
                isLiked ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              ]">
                <Heart :class="isLiked ? 'fill-current' : ''" class="h-4 w-4" />
                <span>{{ article.favorite_count }}</span>
                <span class="text-sm">{{ isLiked ? 'Descurtir' : 'Curtir' }}</span>
              </button>
              
              <button class="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors">
                <Share2 class="h-4 w-4" />
                Compartilhar
              </button>
            </div>
            
            <div class="flex items-center gap-2">
              <span class="text-sm text-gray-600">Avalie este artigo:</span>
              <div class="flex items-center gap-1">
                <button v-for="star in 5" :key="star" 
                       @click="rateArticle(star)"
                       :class="star <= userRating ? 'text-yellow-400' : 'text-gray-300 hover:text-yellow-300'"
                       class="transition-colors">
                  <Star class="h-5 w-5 fill-current" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </article>

      <!-- Comments Section -->
      <div class="mt-8 bg-white rounded-lg shadow-lg p-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">
          Comentários ({{ comments.length }})
        </h2>
        
        <!-- Add Comment Form -->
        <div v-if="isLoggedIn" class="mb-8 p-4 bg-gray-50 rounded-lg">
          <h3 class="text-lg font-semibold mb-4">Deixe seu comentário</h3>
          <form @submit.prevent="addComment" class="space-y-4">
            <textarea 
              v-model="newComment" 
              rows="4" 
              placeholder="Compartilhe sua opinião sobre este artigo..."
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              required
            ></textarea>
            <div class="flex justify-end">
              <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                Publicar Comentário
              </button>
            </div>
          </form>
        </div>
        
        <div v-else class="mb-8 p-4 bg-blue-50 rounded-lg text-center">
          <p class="text-blue-800 mb-3">Faça login para comentar neste artigo</p>
          <button class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            Fazer Login
          </button>
        </div>

        <!-- Comments List -->
        <div class="space-y-6">
          <div v-for="comment in comments" :key="comment.id" class="border-b border-gray-200 pb-6 last:border-b-0">
            <div class="flex items-start gap-4">
              <img :src="comment.userAvatar" :alt="comment.userName" class="w-10 h-10 rounded-full flex-shrink-0">
              <div class="flex-1">
                <div class="flex items-center gap-3 mb-2">
                  <h4 class="font-semibold text-gray-900">{{ comment.userName }}</h4>
                  <span class="text-sm text-gray-500">{{ formatDate(comment.createdAt) }}</span>
                </div>
                <p class="text-gray-700 leading-relaxed">{{ comment.content }}</p>
                
                <div class="flex items-center gap-4 mt-3">
                  <button @click="toggleCommentLike(comment)" :class="[
                    'flex items-center gap-1 text-sm transition-colors',
                    comment.isLiked ? 'text-red-600' : 'text-gray-500 hover:text-red-600'
                  ]">
                    <Heart :class="comment.isLiked ? 'fill-current' : ''" class="h-3 w-3" />
                    {{ comment.likes }}
                  </button>
                  
                  <button class="text-sm text-gray-500 hover:text-blue-600 transition-colors">
                    Responder
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="comments.length === 0" class="text-center py-8">
          <MessageCircle class="h-12 w-12 text-gray-400 mx-auto mb-3" />
          <p class="text-gray-600">Seja o primeiro a comentar este artigo!</p>
        </div>
      </div>

      <!-- Related Articles -->
      <div class="mt-8 bg-white rounded-lg shadow-lg p-6">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">Artigos Relacionados</h2>
        <div class="grid md:grid-cols-2 gap-6">
          <div v-for="relatedArticle in relatedArticles" :key="relatedArticle.id" 
               class="flex gap-4 p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow cursor-pointer"
               @click="$router.push(`/article/${relatedArticle.id}`)">
            <img :src="relatedArticle.image" :alt="relatedArticle.title" class="w-20 h-20 object-cover rounded-lg flex-shrink-0">
            <div>
              <h3 class="font-semibold text-gray-900 mb-1 line-clamp-2">{{ relatedArticle.title }}</h3>
              <p class="text-sm text-gray-600 mb-2">{{ relatedArticle.author }}</p>
              <div class="flex items-center gap-2 text-xs text-gray-500">
                <Star class="h-3 w-3 text-yellow-400 fill-current" />
                <span>{{ relatedArticle.rating }}</span>
                <span>•</span>
                <span>{{ relatedArticle.readTime }} min</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-else class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="bg-white rounded-lg shadow-lg p-8 text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
        <p class="text-gray-600">Carregando artigo...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store';
import articleService from '@/services/articleService';
import { 
  ArrowLeft, 
  Clock, 
  Eye, 
  Star, 
  Heart, 
  Share2, 
  MessageCircle 
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter();
const authStore = useAuthStore();

const isLoading = ref(true);
const article = ref(null)
const error = ref(null)
const isLoggedIn = computed(() => authStore.isAuthenticated); // Should come from auth store
const isLiked = ref(false)
const userRating = ref(0)
const newComment = ref('')
const comments = ref([])

// Function to go back
const goBack = () => router.push('/articles');


// Mock articles data - in real app, fetch from API
const fetchArticleData = async () => {
  isLoading.value = true;
  error.value = null;
  const articleId = route.params.id;

  try {
    const response = await articleService.getArticleDetail(articleId);
    article.value = response.data;
    // Os comentários agora vêm aninhados na resposta do artigo
    comments.value = response.data.comments || [];

    // Verifica se o usuário já curtiu o artigo
    if (isLoggedIn.value) {
      try {
        const favoriteResponse = await articleService.checkFavorite(articleId);
        isLiked.value = favoriteResponse.data.is_favorited;
      } catch (err) {
        console.error("Erro ao verificar favorito:", err);
      }
    }
  } catch (err) {
    console.error("Erro ao buscar o artigo:", err);
    error.value = "Artigo não encontrado ou indisponível.";
    // Opcional: redirecionar para uma página 404
    // router.push('/not-found');
  } finally {
    isLoading.value = false;
  }
};


onMounted(() => {
  fetchArticleData()
})

const addComment = async () => {
  if (!newComment.value.trim() || !article.value) return;
  
  const payload = {
    article: article.value.id,
    comment: newComment.value,
  };

  try {
    // Supondo que você tenha um método 'addComment' no seu serviço
    const response = await articleService.addComment(payload);
    comments.value.unshift(response.data); // Adiciona o novo comentário no topo
    newComment.value = '';
  } catch (err) {
    console.error("Erro ao adicionar comentário:", err);
    alert("Falha ao publicar comentário.");
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('pt-BR', { 
    day: 'numeric', 
    month: 'long', 
    year: 'numeric' 
  }).format(date);
};

const toggleLike = async () => {
  if (!isLoggedIn.value) {
    // Opcional: mostrar mensagem para fazer login
    return;
  }

  try {
    if (isLiked.value) {
      await articleService.unfavorite(article.value.id);
      article.value.favorite_count = Math.max(0, article.value.favorite_count - 1);
    } else {
      await articleService.addFavorite(article.value.id);
      article.value.favorite_count += 1;
    }
    isLiked.value = !isLiked.value;
  } catch (error) {
    console.error('Erro ao atualizar favorito:', error);
    // Opcional: mostrar mensagem de erro para o usuário
  }
}

const rateArticle = (rating) => {
  userRating.value = rating
  // Here you would send the rating to your backend
  console.log('Article rated:', rating)
}

const toggleCommentLike = (comment) => {
  comment.isLiked = !comment.isLiked
  comment.likes += comment.isLiked ? 1 : -1
}
</script>