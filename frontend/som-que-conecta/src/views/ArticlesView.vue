<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Artigos Musicais</h1>
        <p class="text-gray-600">Conteúdo especializado criado por professores e especialistas</p>
      </div>
      
      <router-link 
        v-if="canCreateArticle" 
        to="/articles/create" 
        class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
      >
        <Plus class="h-5 w-5" />
        Novo Artigo
      </router-link>
    </div>

    <!-- Filters -->
    <div class="mb-8 flex flex-wrap gap-4">
      <select v-model="selectedCategory" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option value="">Todas as Categorias</option>
        <option value="teoria">Teoria Musical</option>
        <option value="pratica">Prática</option>
        <option value="instrumentos">Instrumentos</option>
        <option value="historia">História da Música</option>
        <option value="iniciantes">Iniciantes</option>
      </select>
      
      <select v-model="sortBy" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option value="recent">Mais Recentes</option>
        <option value="popular">Mais Populares</option>
        <option value="rating">Melhor Avaliados</option>
        <option value="views">Mais Visualizados</option>
      </select>
      
      <div class="flex-1 max-w-md">
        <div class="relative">
          <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
          <input v-model="searchQuery" type="text" placeholder="Buscar artigos..." class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        </div>
      </div>
    </div>

    <!-- Articles Grid -->
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <article v-for="article in filteredArticles" :key="article.id" class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer" @click="openArticle(article)">
        <div class="relative">
          <img :src="article.image" :alt="article.title" class="w-full h-48 object-cover">
          <div class="absolute top-3 right-3">
            <span class="px-2 py-1 bg-blue-600 text-white text-xs rounded-full font-medium">
              {{ article.category }}
            </span>
          </div>
          <div class="absolute bottom-3 left-3">
            <span class="px-2 py-1 bg-black bg-opacity-70 text-white text-xs rounded-full">
              {{ article.readTime }} min
            </span>
          </div>
        </div>
        
        <div class="p-6">
          <h3 class="text-xl font-semibold text-gray-900 mb-2 line-clamp-2">{{ article.title }}</h3>
          <p class="text-gray-600 mb-4 line-clamp-3">{{ article.excerpt }}</p>
          
          <!-- Article Stats -->
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center gap-4 text-sm text-gray-500">
              <div class="flex items-center gap-1">
                <Eye class="h-4 w-4" />
                <span>{{ formatNumber(article.views) }}</span>
              </div>
              <div class="flex items-center gap-1">
                <MessageCircle class="h-4 w-4" />
                <span>{{ article.commentsCount }}</span>
              </div>
            </div>
            
            <div class="flex items-center gap-1">
              <div class="flex items-center">
                <Star v-for="star in 5" :key="star" 
                     :class="star <= Math.floor(article.rating) ? 'text-yellow-400 fill-current' : 'text-gray-300'"
                     class="h-4 w-4" />
              </div>
              <span class="text-sm text-gray-600 ml-1">({{ article.rating }})</span>
            </div>
          </div>
          
          <!-- Author Info -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <img :src="article.authorAvatar" :alt="article.author" class="w-8 h-8 rounded-full">
              <div>
                <p class="text-sm font-medium text-gray-900">{{ article.author }}</p>
                <p class="text-xs text-gray-500">{{ formatDate(article.createdAt) }}</p>
              </div>
            </div>
            
            <button @click.stop="toggleBookmark(article)" :class="[
              'p-2 rounded-full transition-colors',
              article.isBookmarked ? 'text-blue-600 bg-blue-50' : 'text-gray-400 hover:text-gray-600 hover:bg-gray-50'
            ]">
              <Bookmark :class="article.isBookmarked ? 'fill-current' : ''" class="h-4 w-4" />
            </button>
          </div>
        </div>
      </article>
    </div>

    <!-- Empty State -->
    <div v-if="filteredArticles.length === 0" class="text-center py-12">
      <BookOpen class="h-16 w-16 text-gray-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">Nenhum artigo encontrado</h3>
      <p class="text-gray-600 mb-4">Tente ajustar os filtros ou termos de busca</p>
      <button @click="clearFilters" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
        Limpar Filtros
      </button>
    </div>

    <!-- Load More Button -->
    <div v-if="hasMoreArticles" class="text-center mt-8">
      <button @click="loadMoreArticles" class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
        Carregar Mais Artigos
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Plus, Search, Star, Eye, MessageCircle, Bookmark, BookOpen } from 'lucide-vue-next'

const router = useRouter()
const selectedCategory = ref('')
const sortBy = ref('recent')
const searchQuery = ref('')
const hasMoreArticles = ref(true)

const canCreateArticle = ref(true) // Should check user role

const articles = ref([
  {
    id: 1,
    title: 'Como Escolher Seu Primeiro Instrumento Musical',
    excerpt: 'Descubra os fatores essenciais para escolher o instrumento ideal para começar sua jornada musical. Considerações sobre orçamento, estilo musical preferido e facilidade de aprendizado.',
    category: 'Iniciantes',
    author: 'Ana Carolina',
    authorAvatar: '/placeholder.svg?height=40&width=40',
    rating: 4.8,
    views: 1247,
    commentsCount: 23,
    readTime: 8,
    image: '/placeholder.svg?height=200&width=300',
    createdAt: new Date('2024-01-20'),
    isBookmarked: false
  },
  {
    id: 2,
    title: 'Teoria Musical Básica: Notas, Escalas e Acordes',
    excerpt: 'Entenda os fundamentos da teoria musical de forma simples e prática. Aprenda sobre notas, escalas, acordes e como aplicar esse conhecimento na prática.',
    category: 'Teoria',
    author: 'João Santos',
    authorAvatar: '/placeholder.svg?height=40&width=40',
    rating: 4.9,
    views: 2156,
    commentsCount: 45,
    readTime: 12,
    image: '/placeholder.svg?height=200&width=300',
    createdAt: new Date('2024-01-15'),
    isBookmarked: true
  },
  {
    id: 3,
    title: 'Técnicas de Respiração para Instrumentos de Sopro',
    excerpt: 'Aprenda as técnicas corretas de respiração que são fundamentais para tocar instrumentos de sopro com qualidade e sem fadiga.',
    category: 'Prática',
    author: 'Maria Fernanda',
    authorAvatar: '/placeholder.svg?height=40&width=40',
    rating: 4.7,
    views: 892,
    commentsCount: 18,
    readTime: 6,
    image: '/placeholder.svg?height=200&width=300',
    createdAt: new Date('2024-01-18'),
    isBookmarked: false
  },
  {
    id: 4,
    title: 'História do Jazz: Das Origens aos Dias Atuais',
    excerpt: 'Uma jornada pela rica história do jazz, desde suas origens no sul dos Estados Unidos até as inovações contemporâneas.',
    category: 'História',
    author: 'Carlos Mendes',
    authorAvatar: '/placeholder.svg?height=40&width=40',
    rating: 4.6,
    views: 1534,
    commentsCount: 31,
    readTime: 15,
    image: '/placeholder.svg?height=200&width=300',
    createdAt: new Date('2024-01-12'),
    isBookmarked: false
  },
  {
    id: 5,
    title: 'Manutenção e Cuidados com Instrumentos de Corda',
    excerpt: 'Dicas essenciais para manter seus instrumentos de corda em perfeito estado, prolongando sua vida útil e qualidade sonora.',
    category: 'Instrumentos',
    author: 'Roberto Silva',
    authorAvatar: '/placeholder.svg?height=40&width=40',
    rating: 4.5,
    views: 743,
    commentsCount: 12,
    readTime: 10,
    image: '/placeholder.svg?height=200&width=300',
    createdAt: new Date('2024-01-14'),
    isBookmarked: true
  },
  {
    id: 6,
    title: 'Primeiros Passos no Piano: Postura e Técnica',
    excerpt: 'Fundamentos essenciais para iniciantes no piano, incluindo postura correta, posicionamento das mãos e exercícios básicos.',
    category: 'Iniciantes',
    author: 'Lucia Oliveira',
    authorAvatar: '/placeholder.svg?height=40&width=40',
    rating: 4.9,
    views: 1876,
    commentsCount: 38,
    readTime: 9,
    image: '/placeholder.svg?height=200&width=300',
    createdAt: new Date('2024-01-16'),
    isBookmarked: false
  }
])

const filteredArticles = computed(() => {
  let filtered = articles.value

  // Filter by category
  if (selectedCategory.value) {
    filtered = filtered.filter(article => 
      article.category.toLowerCase().includes(selectedCategory.value.toLowerCase())
    )
  }

  // Filter by search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(article =>
      article.title.toLowerCase().includes(query) ||
      article.excerpt.toLowerCase().includes(query) ||
      article.author.toLowerCase().includes(query)
    )
  }

  // Sort articles
  switch (sortBy.value) {
    case 'popular':
      filtered.sort((a, b) => (b.views + b.commentsCount * 10) - (a.views + a.commentsCount * 10))
      break
    case 'rating':
      filtered.sort((a, b) => b.rating - a.rating)
      break
    case 'views':
      filtered.sort((a, b) => b.views - a.views)
      break
    case 'recent':
    default:
      filtered.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
      break
  }

  return filtered
})

const formatDate = (date) => {
  return new Intl.DateTimeFormat('pt-BR', { 
    day: 'numeric', 
    month: 'short',
    year: 'numeric' 
  }).format(date)
}

const formatNumber = (num) => {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k'
  }
  return num.toString()
}

const openArticle = (article) => {
  // Increment view count
  article.views++
  router.push(`/article/${article.id}`)
}

const toggleBookmark = (article) => {
  article.isBookmarked = !article.isBookmarked
  console.log('Bookmark toggled:', article.id, article.isBookmarked)
}

const clearFilters = () => {
  selectedCategory.value = ''
  sortBy.value = 'recent'
  searchQuery.value = ''
}

const loadMoreArticles = () => {
  // Simulate loading more articles
  console.log('Loading more articles...')
  // In a real app, you would fetch more articles from your API
  hasMoreArticles.value = false
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