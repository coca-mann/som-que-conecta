<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Toast Notification -->
    <div
      v-if="showToast" 
      class="fixed bottom-4 right-4 bg-gray-800 text-white px-6 py-3 rounded-lg shadow-lg transform transition-all duration-300 ease-in-out z-[9999] flex items-center gap-3"
      :class="showToast ? 'translate-y-0 opacity-100' : 'translate-y-2 opacity-0'"
    >
      <span>{{ toastMessage }}</span>
      <button
        class="text-gray-300 hover:text-white transition-colors"
        @click="showToast = false"
      >
        <X class="h-4 w-4" />
      </button>
    </div>

    <!-- Back Navigation -->
    <div class="mb-6">
      <button
        class="flex items-center gap-2 text-blue-600 hover:text-blue-800 transition-colors"
        @click="goBack"
      >
        <ArrowLeft class="h-4 w-4" />
        Voltar aos Artigos
      </button>
    </div>

    <div
      v-if="article"
      class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8"
    >
      <!-- Article Header -->
      <article class="bg-white rounded-lg shadow-lg overflow-hidden">
        <div class="relative h-64 md:h-80">
          <div class="absolute inset-0">
            <img 
              :src="article.cover_image && article.cover_image.includes('default.png') && article.cover_link ? article.cover_link : article.cover_image" 
              :alt="article.title" 
              class="w-full h-full object-cover"
            >
          </div>
          <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent flex items-end">
            <div class="p-6 text-white">
              <div class="flex items-center gap-3 mb-3">
                <span class="px-3 py-1 bg-blue-600 rounded-full text-sm font-medium">
                  {{ article.category?.name || article.category }}
                </span>
                <span class="text-sm opacity-90">{{ formatDate(article.published_at) }}</span>
              </div>
              <h1 class="text-3xl md:text-4xl font-bold leading-tight">
                {{ article.title }}
              </h1>
            </div>
          </div>
        </div>

        <!-- Article Meta -->
        <div class="p-6 border-b border-gray-200">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div class="flex items-center gap-4">
              <img
                :src="article.author.profile_picture"
                :alt="article.author.get_full_name"
                class="w-12 h-12 rounded-full"
              >
              <div>
                <h3 class="font-semibold text-gray-900">
                  {{ article.author.get_full_name }}
                </h3>
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
                <Star
                  v-for="star in 5"
                  :key="star" 
                  :class="star <= Math.floor(article.rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'"
                  class="h-4 w-4"
                />
                <span class="text-sm text-gray-600 ml-1">({{ article.rating }})</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Article Content -->
        <div class="p-6 md:p-8">
          <div class="prose prose-lg max-w-none">
            <p class="text-xl text-gray-600 mb-6 font-medium">
              {{ article.excerpt }}
            </p>
            
            <div
              class="space-y-6 [&>h2]:text-2xl [&>h2]:font-bold [&>h2]:text-gray-900 [&>h2]:mt-8 [&>h2]:mb-4 [&>h3]:text-xl [&>h3]:font-semibold [&>h3]:text-gray-900 [&>h3]:mt-6 [&>h3]:mb-3 [&>p]:text-gray-700 [&>p]:leading-relaxed [&>p]:mb-4 [&>ul]:list-disc [&>ul]:list-inside [&>ul]:space-y-2 [&>ul]:mb-4 [&>ul]:text-gray-700 [&>li]:ml-4 [&>strong]:font-semibold [&>strong]:text-gray-900"
              v-html="article.content"
            />
          </div>
        </div>

        <!-- Article Actions -->
        <div class="p-6 bg-gray-50 border-t border-gray-200">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <button
                :class="[
                  'flex items-center gap-2 px-4 py-2 rounded-lg transition-colors',
                  isLiked ? 'bg-red-100 text-red-600' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                ]"
                @click="toggleLike"
              >
                <Heart
                  :class="isLiked ? 'fill-current' : ''"
                  class="h-4 w-4"
                />
                <span>{{ article.favorite_count }}</span>
                <span class="text-sm">{{ isLiked ? 'Descurtir' : 'Curtir' }}</span>
              </button>
              
              <button
                class="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
                @click="shareArticle"
              >
                <Share2 class="h-4 w-4" />
                Compartilhar
              </button>
            </div>
            
            <div class="flex items-center gap-2">
              <span class="text-sm text-gray-600">Avalie este artigo:</span>
              <div class="flex items-center gap-1">
                <button
                  v-for="star in 5"
                  :key="star" 
                  :class="star <= userRating ? 'text-yellow-400' : 'text-gray-300 hover:text-yellow-300'"
                  class="transition-colors"
                  @click="rateArticle(star)"
                >
                  <Star class="h-5 w-5 fill-current" />
                </button>
                <button
                  v-if="userRating" 
                  class="ml-2 text-sm text-gray-500 hover:text-red-600 transition-colors"
                  @click="removeRating"
                >
                  Remover avaliação
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
        <div
          v-if="isLoggedIn"
          class="mb-8 p-4 bg-gray-50 rounded-lg"
        >
          <div class="mb-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <p class="text-sm text-blue-800">
              <span class="font-medium">Atenção:</span> Os comentários são moderados e podem ser removidos caso não estejam de acordo com nossas diretrizes de comunidade.
            </p>
          </div>
          <h3 class="text-lg font-semibold mb-4">
            Deixe seu comentário
          </h3>
          <form
            class="space-y-4"
            @submit.prevent="addComment"
          >
            <textarea 
              v-model="newComment" 
              rows="4" 
              placeholder="Compartilhe sua opinião sobre este artigo..."
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              :disabled="isSubmittingComment"
              required
            />
            <div class="flex justify-end">
              <button 
                type="submit" 
                class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
                :disabled="isSubmittingComment"
              >
                <div
                  v-if="isSubmittingComment"
                  class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"
                />
                {{ isSubmittingComment ? 'Enviando...' : 'Publicar Comentário' }}
              </button>
            </div>
          </form>
        </div>
        
        <div
          v-else
          class="mb-8 p-4 bg-blue-50 rounded-lg text-center"
        >
          <p class="text-blue-800 mb-3">
            Faça login para comentar neste artigo
          </p>
          <button class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            Fazer Login
          </button>
        </div>

        <!-- Comments List -->
        <div class="space-y-6">
          <div
            v-for="comment in comments"
            :key="comment.id"
            class="border-b border-gray-200 pb-6 last:border-b-0"
          >
            <div class="flex items-start gap-4">
              <img
                :src="comment.userAvatar"
                :alt="comment.userName"
                class="w-10 h-10 rounded-full flex-shrink-0"
              >
              <div class="flex-1">
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-3">
                    <h4 class="font-semibold text-gray-900">
                      {{ comment.userName }}
                    </h4>
                    <span class="text-sm text-gray-500">{{ formatDate(comment.createdAt) }}</span>
                  </div>
                  <button 
                    v-if="isCommentAuthor(comment) || isAdmin"
                    class="p-1 text-gray-400 hover:text-red-600 transition-colors rounded-full hover:bg-red-50"
                    title="Excluir comentário"
                    @click="confirmDeleteComment(comment)"
                  >
                    <Trash2 class="h-4 w-4" />
                  </button>
                </div>
                <p class="text-gray-700 leading-relaxed">
                  {{ comment.content }}
                </p>
              </div>
            </div>
          </div>
        </div>
        
        <div
          v-if="comments.length === 0"
          class="text-center py-8"
        >
          <MessageCircle class="h-12 w-12 text-gray-400 mx-auto mb-3" />
          <p class="text-gray-600">
            Seja o primeiro a comentar este artigo!
          </p>
        </div>
      </div>
    </div>
    
    <!-- Loading State -->
    <div
      v-else
      class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8"
    >
      <div class="bg-white rounded-lg shadow-lg p-8 text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4" />
        <p class="text-gray-600">
          Carregando artigo...
        </p>
      </div>
    </div>

    <!-- Delete Comment Confirmation Modal -->
    <div
      v-if="showDeleteCommentModal"
      class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50"
    >
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <div class="text-center">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <AlertTriangle class="h-8 w-8 text-red-600" />
          </div>
          <h3 class="text-lg font-semibold mb-2">
            Confirmar Exclusão
          </h3>
          <p class="text-gray-600 mb-6">
            Tem certeza que deseja excluir este comentário? 
            Esta ação não pode ser desfeita.
          </p>
          <div class="flex gap-3 justify-center">
            <button 
              class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors" 
              :disabled="isDeletingComment"
              @click="showDeleteCommentModal = false"
            >
              Cancelar
            </button>
            <button 
              class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2" 
              :disabled="isDeletingComment"
              @click="deleteComment"
            >
              <div
                v-if="isDeletingComment"
                class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"
              />
              {{ isDeletingComment ? 'Excluindo...' : 'Excluir' }}
            </button>
          </div>
        </div>
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
  MessageCircle,
  Trash2,
  AlertTriangle,
  X
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter();
const authStore = useAuthStore();

const isLoading = ref(true);
const article = ref(null)
const error = ref(null)
const isLoggedIn = computed(() => authStore.isAuthenticated);
const isLiked = ref(false)
const userRating = ref(0)
const newComment = ref('')
const comments = ref([])
const showToast = ref(false)
const toastMessage = ref('')
const showDeleteCommentModal = ref(false)
const commentToDelete = ref(null)
const isDeletingComment = ref(false)
const isAdmin = computed(() => authStore.user?.is_staff || false)
const isSubmittingComment = ref(false)

// Function to go back
const goBack = () => router.push('/articles');

// Função para verificar a avaliação do usuário
const checkUserRating = async () => {
  if (!isLoggedIn.value || !article.value) return;
  
  try {
    const response = await articleService.checkRating(article.value.id);
    if (response.data.has_rated) {
      userRating.value = response.data.rating;
    }
  } catch (error) {
    console.error('Erro ao verificar avaliação do usuário:', error);
  }
};

// Atualizar o fetchArticleData para incluir a verificação de avaliação
const fetchArticleData = async () => {
  isLoading.value = true;
  error.value = null;
  const articleId = route.params.id;

  // Rola a página para o topo
  window.scrollTo({ top: 0, behavior: 'smooth' });

  try {
    const response = await articleService.getArticleDetail(articleId);
    article.value = response.data;
    
    // Carregar comentários separadamente
    await loadComments();

    // Verifica se o usuário já curtiu o artigo
    if (isLoggedIn.value) {
      try {
        const favoriteResponse = await articleService.checkFavorite(articleId);
        isLiked.value = favoriteResponse.data.is_favorited;
        
        // Verificar a avaliação do usuário
        await checkUserRating();
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

// Função para carregar comentários
const loadComments = async () => {
  if (!article.value) return;
  
  try {
    const response = await articleService.getComments(article.value.id);
    comments.value = response.data;
  } catch (err) {
    console.error("Erro ao carregar comentários:", err);
  }
};

onMounted(() => {
  fetchArticleData()
})

const addComment = async () => {
  if (!newComment.value.trim() || !article.value) return;
  
  isSubmittingComment.value = true;
  try {
    const response = await articleService.addComment(article.value.id, newComment.value);
    
    // Verifica se o comentário foi aprovado pela IA
    if (!response.data.is_published) {
      showToastMessage(response.data.ai_feedback || 'Seu comentário não foi aprovado pela moderação.');
      return;
    }
    
    comments.value.unshift(response.data);
    newComment.value = '';
    showToastMessage('Comentário publicado com sucesso!');
  } catch (err) {
    console.error("Erro ao adicionar comentário:", err);
    showToastMessage("Falha ao publicar comentário. Por favor, tente novamente.");
  } finally {
    isSubmittingComment.value = false;
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

const rateArticle = async (rating) => {
  if (!isLoggedIn.value) {
    alert('Por favor, faça login para avaliar este artigo.');
    return;
  }

  try {
    const response = await articleService.rateArticle(article.value.id, rating);
    article.value.rating = response.data.rating;
    userRating.value = rating;
  } catch (error) {
    console.error('Erro ao avaliar artigo:', error);
    alert('Erro ao registrar sua avaliação. Por favor, tente novamente.');
  }
}

const removeRating = async () => {
  if (!isLoggedIn.value || !article.value) return;
  
  try {
    const response = await articleService.removeRating(article.value.id);
    article.value.rating = response.data.rating;
    userRating.value = 0;
  } catch (error) {
    console.error('Erro ao remover avaliação:', error);
    alert('Erro ao remover sua avaliação. Por favor, tente novamente.');
  }
};

// Função para mostrar o toast
const showToastMessage = (message) => {
  toastMessage.value = message
  showToast.value = true
}

// Função para compartilhar o artigo
const shareArticle = async () => {
  const shareData = {
    title: article.value.title,
    text: article.value.short_description,
    url: window.location.href
  }

  try {
    if (navigator.share) {
      // Web Share API está disponível
      await navigator.share(shareData)
    } else {
      // Fallback: copiar link para a área de transferência
      await navigator.clipboard.writeText(window.location.href)
      showToastMessage('Link copiado para a área de transferência!')
    }
  } catch (error) {
    if (error.name !== 'AbortError') {
      console.error('Erro ao compartilhar:', error)
      showToastMessage('Erro ao compartilhar o artigo')
    }
  }
}

const isCommentAuthor = (comment) => {
  return comment.user?.id === authStore.user?.id
}

const confirmDeleteComment = (comment) => {
  commentToDelete.value = comment
  showDeleteCommentModal.value = true
}

const deleteComment = async () => {
  if (!commentToDelete.value) return
  
  isDeletingComment.value = true
  try {
    await articleService.deleteComment(route.params.id, commentToDelete.value.id)
    comments.value = comments.value.filter(c => c.id !== commentToDelete.value.id)
    showDeleteCommentModal.value = false
    commentToDelete.value = null
    showToastMessage('Comentário excluído com sucesso!')
  } catch (error) {
    console.error('Erro ao excluir comentário:', error)
    showToastMessage('Erro ao excluir comentário. Tente novamente.')
  } finally {
    isDeletingComment.value = false
  }
}
</script>