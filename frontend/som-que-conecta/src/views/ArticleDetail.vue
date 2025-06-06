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
          <img :src="article.image" :alt="article.title" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-black bg-opacity-40 flex items-end">
            <div class="p-6 text-white">
              <div class="flex items-center gap-3 mb-3">
                <span class="px-3 py-1 bg-blue-600 rounded-full text-sm font-medium">
                  {{ article.category }}
                </span>
                <span class="text-sm opacity-90">{{ formatDate(article.createdAt) }}</span>
              </div>
              <h1 class="text-3xl md:text-4xl font-bold leading-tight">{{ article.title }}</h1>
            </div>
          </div>
        </div>

        <!-- Article Meta -->
        <div class="p-6 border-b border-gray-200">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div class="flex items-center gap-4">
              <img :src="article.authorAvatar" :alt="article.author" class="w-12 h-12 rounded-full">
              <div>
                <h3 class="font-semibold text-gray-900">{{ article.author }}</h3>
                <p class="text-sm text-gray-600">{{ article.authorRole }}</p>
              </div>
            </div>
            
            <div class="flex items-center gap-6">
              <div class="flex items-center gap-2">
                <Clock class="h-4 w-4 text-gray-500" />
                <span class="text-sm text-gray-600">{{ article.readTime }} min de leitura</span>
              </div>
              
              <div class="flex items-center gap-2">
                <Eye class="h-4 w-4 text-gray-500" />
                <span class="text-sm text-gray-600">{{ article.views }} visualizações</span>
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
            
            <div v-html="article.content" class="space-y-6"></div>
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
                <span>{{ article.likes + (isLiked ? 1 : 0) }}</span>
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
import { useRoute } from 'vue-router'
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
const article = ref(null)
const isLoggedIn = ref(false) // Should come from auth store
const isLiked = ref(false)
const userRating = ref(0)
const newComment = ref('')
const comments = ref([])

// Function to go back
const goBack = () => {
  window.history.go(-1)
}

// Mock articles data - in real app, fetch from API
const articlesData = {
  1: {
    id: 1,
    title: 'Como Escolher Seu Primeiro Instrumento Musical',
    excerpt: 'Descubra os fatores essenciais para escolher o instrumento ideal para começar sua jornada musical. Considerações sobre orçamento, estilo musical preferido e facilidade de aprendizado.',
    content: `
      <h2>Introdução</h2>
      <p>Escolher seu primeiro instrumento musical é uma decisão importante que pode definir toda sua jornada musical. Este guia completo vai te ajudar a tomar a melhor decisão baseada em seus objetivos, orçamento e preferências pessoais.</p>
      
      <h2>Fatores a Considerar</h2>
      <h3>1. Orçamento Disponível</h3>
      <p>O orçamento é um dos fatores mais importantes na escolha do seu primeiro instrumento. Instrumentos de qualidade podem variar drasticamente de preço:</p>
      <ul>
        <li><strong>Violão:</strong> R$ 200 - R$ 2.000+</li>
        <li><strong>Teclado:</strong> R$ 300 - R$ 3.000+</li>
        <li><strong>Flauta:</strong> R$ 150 - R$ 1.500+</li>
        <li><strong>Bateria:</strong> R$ 800 - R$ 5.000+</li>
      </ul>
      
      <h3>2. Estilo Musical Preferido</h3>
      <p>Seu gosto musical deve influenciar diretamente sua escolha:</p>
      <ul>
        <li><strong>Rock/Pop:</strong> Guitarra elétrica, baixo, bateria</li>
        <li><strong>Clássico:</strong> Piano, violino, flauta</li>
        <li><strong>Folk/Country:</strong> Violão, harmônica, banjo</li>
        <li><strong>Jazz:</strong> Saxofone, piano, contrabaixo</li>
      </ul>
      
      <h2>Instrumentos Recomendados para Iniciantes</h2>
      <h3>Violão</h3>
      <p>O violão é uma excelente escolha para iniciantes devido à sua versatilidade e facilidade de transporte. Com apenas alguns acordes básicos, você já pode tocar centenas de músicas.</p>
      
      <h3>Piano/Teclado</h3>
      <p>O piano oferece uma base sólida em teoria musical e é fundamental para entender harmonia. Teclados modernos oferecem muitas funcionalidades a um preço acessível.</p>
      
      <h3>Ukulele</h3>
      <p>Menor e mais simples que o violão, o ukulele é perfeito para crianças ou adultos que querem resultados rápidos. Com apenas 4 cordas, é mais fácil de dominar.</p>
      
      <h2>Dicas Finais</h2>
      <p>Lembre-se: o melhor instrumento é aquele que você vai praticar regularmente. Escolha algo que te inspire e motive a continuar aprendendo. Considere também a possibilidade de alugar um instrumento antes de comprar, especialmente para instrumentos mais caros.</p>
    `,
    category: 'Iniciantes',
    author: 'Ana Carolina',
    authorRole: 'Professora de Música',
    authorAvatar: '/placeholder.svg?height=50&width=50',
    rating: 4.9,
    readTime: 8,
    views: 1247,
    likes: 89,
    createdAt: new Date('2024-01-20'),
    image: '/placeholder.svg?height=400&width=800'
  },
  2: {
    id: 2,
    title: 'Teoria Musical Básica: Notas, Escalas e Acordes',
    excerpt: 'Entenda os fundamentos da teoria musical de forma simples e prática. Aprenda sobre notas, escalas, acordes e como aplicar esse conhecimento na prática.',
    content: `
      <h2>O que é Teoria Musical?</h2>
      <p>A teoria musical é a linguagem que usamos para descrever e entender a música. É como a gramática para um idioma - nos ajuda a comunicar ideias musicais de forma clara e precisa.</p>
      
      <h2>As Notas Musicais</h2>
      <p>Existem 12 notas diferentes na música ocidental, que se repetem em diferentes oitavas:</p>
      <p><strong>Dó - Dó# - Ré - Ré# - Mi - Fá - Fá# - Sol - Sol# - Lá - Lá# - Si</strong></p>
      
      <h2>Escalas Musicais</h2>
      <p>Uma escala é uma sequência de notas organizadas em ordem ascendente ou descendente. A escala mais comum é a escala maior, que segue o padrão:</p>
      <p><strong>Tom - Tom - Semitom - Tom - Tom - Tom - Semitom</strong></p>
      
      <h2>Acordes Básicos</h2>
      <p>Um acorde é formado por três ou mais notas tocadas simultaneamente. Os acordes básicos incluem:</p>
      <ul>
        <li><strong>Acorde Maior:</strong> 1ª - 3ª maior - 5ª justa</li>
        <li><strong>Acorde Menor:</strong> 1ª - 3ª menor - 5ª justa</li>
        <li><strong>Acorde Diminuto:</strong> 1ª - 3ª menor - 5ª diminuta</li>
      </ul>
    `,
    category: 'Teoria',
    author: 'João Santos',
    authorRole: 'Professor de Teoria Musical',
    authorAvatar: '/placeholder.svg?height=50&width=50',
    rating: 4.7,
    readTime: 12,
    views: 892,
    likes: 67,
    createdAt: new Date('2024-01-15'),
    image: '/placeholder.svg?height=400&width=800'
  }
}

const relatedArticles = ref([
  {
    id: 2,
    title: 'Teoria Musical Básica: Notas, Escalas e Acordes',
    author: 'João Santos',
    rating: 4.7,
    readTime: 12,
    image: '/placeholder.svg?height=80&width=80'
  },
  {
    id: 3,
    title: 'Técnicas de Respiração para Instrumentos de Sopro',
    author: 'Maria Fernanda',
    rating: 4.8,
    readTime: 6,
    image: '/placeholder.svg?height=80&width=80'
  }
])

const mockComments = [
  {
    id: 1,
    userName: 'Carlos Silva',
    userAvatar: '/placeholder.svg?height=40&width=40',
    content: 'Excelente artigo! Me ajudou muito a decidir entre violão e piano. Acabei escolhendo o violão e estou adorando as aulas.',
    likes: 12,
    isLiked: false,
    createdAt: new Date('2024-01-21')
  },
  {
    id: 2,
    userName: 'Fernanda Costa',
    userAvatar: '/placeholder.svg?height=40&width=40',
    content: 'Muito útil! Gostaria de ver mais conteúdo sobre instrumentos de sopro também.',
    likes: 8,
    isLiked: true,
    createdAt: new Date('2024-01-22')
  }
]

const formatDate = (date) => {
  return new Intl.DateTimeFormat('pt-BR', { 
    day: 'numeric', 
    month: 'long', 
    year: 'numeric' 
  }).format(date)
}

const toggleLike = () => {
  isLiked.value = !isLiked.value
}

const rateArticle = (rating) => {
  userRating.value = rating
  // Here you would send the rating to your backend
  console.log('Article rated:', rating)
}

const addComment = () => {
  if (!newComment.value.trim()) return
  
  const comment = {
    id: Date.now(),
    userName: 'Usuário Atual', // Should come from auth store
    userAvatar: '/placeholder.svg?height=40&width=40',
    content: newComment.value,
    likes: 0,
    isLiked: false,
    createdAt: new Date()
  }
  
  comments.value.unshift(comment)
  newComment.value = ''
}

const toggleCommentLike = (comment) => {
  comment.isLiked = !comment.isLiked
  comment.likes += comment.isLiked ? 1 : -1
}

onMounted(() => {
  const articleId = parseInt(route.params.id)
  article.value = articlesData[articleId]
  comments.value = [...mockComments]
  
  if (!article.value) {
    // Handle article not found
    console.error('Article not found')
  }
})
</script>

<style scoped>
.prose h2 {
  @apply text-2xl font-bold text-gray-900 mt-8 mb-4;
}

.prose h3 {
  @apply text-xl font-semibold text-gray-900 mt-6 mb-3;
}

.prose p {
  @apply text-gray-700 leading-relaxed mb-4;
}

.prose ul {
  @apply list-disc list-inside space-y-2 mb-4 text-gray-700;
}

.prose li {
  @apply ml-4;
}

.prose strong {
  @apply font-semibold text-gray-900;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>