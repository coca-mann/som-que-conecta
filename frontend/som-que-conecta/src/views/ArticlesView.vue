<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">
          Artigos Musicais
        </h1>
        <p class="text-gray-600">
          Conteúdo especializado criado por professores e especialistas
        </p>
      </div>
      
      <router-link 
        v-if="canCreateArticle" 
        to="/articles/create" 
        class="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2"
      >
        <Plus class="h-5 w-5" />
        Novo Artigo
      </router-link>
    </div>

    <div class="flex gap-4 mb-6">
      <select
        v-model="selectedCategory"
        class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
      >
        <option value="">
          Todas as Categorias
        </option>
        
        <option 
          v-for="category in categories" 
          :key="category.id" 
          :value="category.name"
        >
          {{ category.name }}
        </option>
      </select>
      
      <select
        v-model="sortBy"
        class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
      >
        <option value="-created_at">
          Mais Recentes
        </option>
        <option value="-popularity">
          Mais Populares
        </option>
        <option value="-rating">
          Melhor Avaliados
        </option>
        <option value="-read_count">
          Mais Visualizados
        </option>
      </select>
      
      <div class="flex-1 max-w-md">
        <div class="relative">
          <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Buscar artigos..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
          >
        </div>
      </div>
    </div>

    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <article
        v-for="article in filteredArticles"
        :key="article.id"
        class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
        @click="openArticle(article)"
      >
        <div class="relative">
          <img 
            :src="article.cover_image && article.cover_image.includes('default.png') && article.cover_link ? article.cover_link : article.cover_image" 
            :alt="article.title" 
            class="w-full h-48 object-cover"
          >
          
          <div
            v-if="!article.is_published"
            class="absolute inset-0 bg-gray-900 bg-opacity-70 flex flex-col items-center justify-center text-white p-4"
          >
            <EyeOff class="h-8 w-8 mb-2" />
            <span class="font-bold text-lg">Não Publicado</span>
            <span class="text-sm opacity-80">(Visível apenas para você)</span>
          </div>
          
          <div class="absolute top-3 right-3">
            <span class="px-2 py-1 bg-red-600 text-white text-xs rounded-full font-medium">
              {{ article.category || 'Sem categoria' }}
            </span>
          </div>
          <div class="absolute bottom-3 left-3">
            <span class="px-2 py-1 bg-black bg-opacity-70 text-white text-xs rounded-full">
              {{ article.reading_time }} min
            </span>
          </div>
        </div>
        
        <div class="p-6">
          <h3 class="text-xl font-semibold text-gray-900 mb-2 line-clamp-2">
            {{ article.title }}
          </h3>
          <p class="text-gray-600 mb-4 line-clamp-3">
            {{ article.excerpt }}
          </p>
          
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-4 text-sm text-gray-500">
              <div class="flex items-center gap-1">
                <Eye class="h-4 w-4" />
                <span>{{ formatNumber(article.read_count) }}</span>
              </div>
              <div class="flex items-center gap-1">
                <MessageCircle class="h-4 w-4" />
                <span>{{ article.comments_count }}</span>
              </div>
            </div>
            
            <div class="flex items-center gap-1">
              <div class="flex items-center">
                <Star
                  v-for="star in 5"
                  :key="star" 
                  :class="star <= Math.floor(article.rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'"
                  class="h-4 w-4"
                />
              </div>
              <span class="text-sm text-gray-600 ml-1">({{ article.rating }})</span>
            </div>
          </div>
          
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <img
                :src="article.author?.profile_picture"
                :alt="article.author?.get_full_name"
                class="w-8 h-8 rounded-full"
              >
              <div>
                <p class="text-sm font-medium text-gray-900">
                  {{ article.author?.get_full_name }}
                </p>
                <p class="text-xs text-gray-500">
                  {{ formatDate(article.created_at) }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </article>
    </div>

    <div
      v-if="filteredArticles.length === 0"
      class="text-center py-12"
    >
      <BookOpen class="h-16 w-16 text-gray-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">
        Nenhum artigo encontrado
      </h3>
      <p class="text-gray-600 mb-4">
        Tente ajustar os filtros ou termos de busca
      </p>
      <button
        class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        @click="clearFilters"
      >
        Limpar Filtros
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth.store';
import articleService from '@/services/articleService';
import { Plus, Search, Star, Eye, MessageCircle, BookOpen } from 'lucide-vue-next'
import { useHead } from '@vueuse/head';

useHead({
  title: 'Artigos | Som que Conecta',
  meta: [
    { name: 'description', content: 'Leia artigos sobre teoria musical, prática e instrumentos.' },
  ]
})

const router = useRouter()
const authStore = useAuthStore();

const selectedCategory = ref('')
const sortBy = ref('-created_at')
const searchQuery = ref('')

// Permissão para criar
const canCreateArticle = computed(() => {
    // Exemplo: apenas professores ou admins podem criar
    const userRole = authStore.user?.role;
    return ['professor', 'admin', 'ong'].includes(userRole);
});

const articles = ref([]);
const categories = ref([]);
const isLoading = ref(true);

// Função de busca
const fetchArticles = async () => {
  isLoading.value = true;
  const params = {
    category: selectedCategory.value,
    search: searchQuery.value,
    ordering: sortBy.value,
  };
  try {
    const response = await articleService.getArticles(params);
    articles.value = response.data; // A API deve retornar uma lista paginada
  } catch (error) {
    console.error("Erro ao buscar artigos:", error);
  } finally {
    isLoading.value = false;
  }
};

const fetchCategories = async () => {
    try {
        const response = await articleService.getCategories();
        categories.value = response.data; // Armazena os resultados na ref
    } catch (e) {
        console.error("Erro ao buscar categorias:", e);
    }
};

// Observa mudanças nos filtros para buscar novamente
watch([selectedCategory, sortBy, searchQuery], fetchArticles);

// Busca inicial
onMounted(() => {
  fetchArticles();
  fetchCategories();
});

const openArticle = (article) => {
  // Verificamos o status de publicação do artigo
  if (article.is_published) {
    // Se estiver publicado, navega para a página de leitura normal
    console.log(`Navegando para a leitura do artigo publicado: ${article.id}`);
    router.push(`/articles/${article.id}`);
  } else {
    // Se NÃO estiver publicado (é um rascunho), navega para a página de edição
    console.log(`Navegando para a edição do rascunho: ${article.id}`);
    router.push(`/articles/edit/${article.id}`);
  }
};

const filteredArticles = computed(() => {
  let filtered = articles.value

  // Filter by category
  if (selectedCategory.value) {
    filtered = filtered.filter(article => 
      article.category?.toLowerCase() === selectedCategory.value.toLowerCase()
    )
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(article =>
      article.title.toLowerCase().includes(query) ||
      article.short_description?.toLowerCase().includes(query) ||
      article.author?.get_full_name?.toLowerCase().includes(query)
    )
  }

  // Sort articles
  switch (sortBy.value) {
    case '-popularity':
      filtered.sort((a, b) => (b.read_count + b.comments_count * 10) - (a.read_count + a.comments_count * 10))
      break
    case '-rating':
      filtered.sort((a, b) => b.rating - a.rating)
      break
    case '-read_count':
      filtered.sort((a, b) => b.read_count - a.read_count)
      break
    case '-created_at':
    default:
      filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      break
  }

  return filtered
})

const formatDate = (date) => {
  if (!date) return '';
  
  try {
    const dateObj = new Date(date);
    if (isNaN(dateObj.getTime())) return '';
    
    return new Intl.DateTimeFormat('pt-BR', { 
      day: 'numeric', 
      month: 'short',
      year: 'numeric' 
    }).format(dateObj);
  } catch (error) {
    console.error('Erro ao formatar data:', error);
    return '';
  }
}

const formatNumber = (num) => {
  // Se o número for nulo ou indefinido, retorna '0' para não quebrar.
  if (num === null || num === undefined) {
    return '0';
  }
  
  if (num >= 1000) {
    return (num / 1000).toFixed(1).replace('.', ',') + 'k';
  }
  
  return num.toString();
};

const clearFilters = () => {
  selectedCategory.value = ''
  sortBy.value = 'recent'
  searchQuery.value = ''
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>