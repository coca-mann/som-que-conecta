<template>
  <main class="relative min-h-screen">
    <div class="fixed inset-0 w-full h-full">
      <img
        src="@/assets/homebackground.jpg"
        alt="Background Pattern"
        class="w-full h-full object-cover opacity-20"
      >
    </div>

    <section class="relative py-24 overflow-hidden">
      <div class="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center">
          <h1
            class="text-4xl font-extrabold text-gray-900 sm:text-5xl lg:text-6xl"
          >
            Aprenda Música do Zero
          </h1>
          <p
            class="mt-4 max-w-2xl mx-auto text-xl text-gray-600 sm:mt-5 sm:text-2xl"
          >
            Descubra o prazer de tocar um instrumento com nossos cursos e
            artigos especializados.
          </p>
          <div class="mt-8 flex justify-center space-x-3 sm:mt-12">
            <router-link
              to="/courses"
              class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
            >
              Começar Agora
            </router-link>
            <router-link
              to="/articles"
              class="inline-flex items-center justify-center px-5 py-3 text-base font-medium rounded-md text-red-700 bg-red-100 hover:bg-red-200"
            >
              Ler Artigos
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <section class="py-16 bg-white/90 backdrop-blur-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">
            Tudo que Você Precisa para Começar
          </h2>
          <p class="text-xl text-gray-600 max-w-2xl mx-auto">
            Nossa plataforma oferece recursos completos para iniciantes na música
          </p>
        </div>
        
        <div class="grid md:grid-cols-3 gap-8">
          <div class="text-center p-6 rounded-lg border border-gray-200 hover:shadow-lg transition-shadow">
            <BookOpen class="h-12 w-12 text-red-600 mx-auto mb-4" />
            <h3 class="text-xl font-semibold mb-2">
              Artigos Especializados
            </h3>
            <p class="text-gray-600">
              Conteúdo criado por professores experientes para guiar seu aprendizado
            </p>
          </div>
          
          <div class="text-center p-6 rounded-lg border border-gray-200 hover:shadow-lg transition-shadow">
            <Guitar class="h-12 w-12 text-red-600 mx-auto mb-4" />
            <h3 class="text-xl font-semibold mb-2">
              Instrumentos Disponíveis
            </h3>
            <p class="text-gray-600">
              Acesse instrumentos musicais disponibilizados por ONGs e professores
            </p>
          </div>
          
          <div class="text-center p-6 rounded-lg border border-gray-200 hover:shadow-lg transition-shadow">
            <GraduationCap class="h-12 w-12 text-red-600 mx-auto mb-4" />
            <h3 class="text-xl font-semibold mb-2">
              Minicursos Práticos
            </h3>
            <p class="text-gray-600">
              Aprenda passo a passo com cursos estruturados e acompanhe seu progresso
            </p>
          </div>
        </div>
      </div>
    </section>

    <section class="py-16 bg-gradient-to-br from-red-100 to-red-200 backdrop-blur-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">
            Artigo Mais Recente
          </h2>
          <p class="text-xl text-gray-600">
            Confira o último conteúdo publicado por nossos especialistas
          </p>
        </div>
        
        <div class="max-w-4xl mx-auto">
          <div
            v-if="isLoading"
            class="flex justify-center items-center h-64"
          >
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600" />
          </div>
          
          <div
            v-else-if="latestArticle"
            class="bg-white rounded-2xl shadow-xl overflow-hidden hover:shadow-2xl transition-shadow duration-300"
          >
            <div class="md:flex">
              <div class="md:w-1/2">
                <img 
                  :src="latestArticle.cover_image && !latestArticle.cover_image.includes('default.png') 
                    ? homeService.getImageUrl(latestArticle.cover_image) 
                    : latestArticle.cover_link" 
                  :alt="latestArticle.title" 
                  class="w-full h-64 md:h-full object-cover"
                >
              </div>
              <div class="md:w-1/2 p-8">
                <div class="flex items-center gap-3 mb-4">
                  <span class="px-3 py-1 bg-red-100 text-red-800 text-sm rounded-full font-medium">
                    {{ latestArticle.category }}
                  </span>
                  <div class="flex items-center text-yellow-500">
                    <Star class="h-4 w-4 fill-current" />
                    <span class="text-sm text-gray-600 ml-1">{{ latestArticle.rating }}</span>
                  </div>
                  <span class="text-sm text-gray-500">{{ formatDate(latestArticle.created_at) }}</span>
                </div>
                
                <h3 class="text-2xl font-bold text-gray-900 mb-4">
                  {{ latestArticle.title }}
                </h3>
                <p class="text-gray-600 mb-6 leading-relaxed">
                  {{ latestArticle.short_description }}
                </p>
                
                <div class="flex items-center justify-between mb-6">
                  <div class="flex items-center gap-3">
                    <img
                      :src="homeService.getImageUrl(latestArticle.author.profile_picture)"
                      :alt="latestArticle.author.get_full_name"
                      class="w-10 h-10 rounded-full"
                    >
                    <div>
                      <p class="font-medium text-gray-900">
                        {{ latestArticle.author.get_full_name }}
                      </p>
                      <p class="text-sm text-gray-500">
                        Autor
                      </p>
                    </div>
                  </div>
                  <div class="flex items-center gap-2 text-sm text-gray-500">
                    <Clock class="h-4 w-4" />
                    <span>{{ latestArticle.reading_time }} min</span>
                  </div>
                </div>
                
                <router-link
                  :to="`/articles/${latestArticle.id}`"
                  class="inline-flex items-center gap-2 px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
                >
                  Ler Artigo Completo
                  <ArrowRight class="h-4 w-4" />
                </router-link>
              </div>
            </div>
          </div>
          
          <div
            v-else
            class="text-center py-12"
          >
            <p class="text-gray-600">
              Nenhum artigo disponível no momento.
            </p>
          </div>
        </div>
      </div>
    </section>

    <section class="py-16 bg-gradient-to-br from-gray-200 to-red-100 backdrop-blur-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-gray-900 mb-4">
            Curso Mais Recente
          </h2>
          <p class="text-xl text-gray-600">
            Descubra o último minicurso adicionado à nossa plataforma
          </p>
        </div>
        
        <div class="max-w-4xl mx-auto">
          <div
            v-if="isLoading"
            class="flex justify-center items-center h-64"
          >
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600" />
          </div>
          
          <div
            v-else-if="latestCourse"
            class="bg-white rounded-2xl shadow-xl overflow-hidden hover:shadow-2xl transition-shadow duration-300"
          >
            <div class="md:flex md:flex-row-reverse">
              <div class="md:w-1/2">
                <img
                  :src="latestCourse.cover"
                  :alt="latestCourse.title"
                  class="w-full h-64 md:h-full object-cover"
                >
              </div>
              <div class="md:w-1/2 p-8">
                <div class="flex items-center gap-3 mb-4">
                  <span class="px-3 py-1 bg-gray-200 text-gray-800 text-sm rounded-full font-medium">
                    {{ latestCourse.skill_level_display }}
                  </span>
                  <span class="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full font-medium">
                    {{ latestCourse.instrument_type_name }}
                  </span>
                  <span class="text-sm text-gray-500">Novo!</span>
                </div>
                
                <h3 class="text-2xl font-bold text-gray-900 mb-4">
                  {{ latestCourse.title }}
                </h3>
                <p class="text-gray-600 mb-6 leading-relaxed">
                  {{ latestCourse.description }}
                </p>
                
                <div class="grid grid-cols-2 gap-4 mb-6">
                  <div class="flex items-center gap-2 text-sm text-gray-600">
                    <Clock class="h-4 w-4 text-red-600" />
                    <span>{{ latestCourse.duration_display }}</span>
                  </div>
                  <div class="flex items-center gap-2 text-sm text-gray-600">
                    <BookOpen class="h-4 w-4 text-red-600" />
                    <span>{{ latestCourse.tasks_count }} aulas</span>
                  </div>
                </div>
                
                <div
                  v-if="latestCourse.author"
                  class="flex items-center gap-3 mb-6"
                >
                  <img
                    :src="homeService.getImageUrl(latestCourse.author.profile_picture)"
                    :alt="latestCourse.author.name"
                    class="w-10 h-10 rounded-full"
                  >
                  <div>
                    <p class="font-medium text-gray-900">
                      {{ latestCourse.author.name }}
                    </p>
                    <p class="text-sm text-gray-500">
                      Instrutor
                    </p>
                  </div>
                </div>
                
                <div class="flex gap-3">
                  <router-link
                    :to="`/course/${latestCourse.id}`"
                    class="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
                  >
                    {{ isLoggedIn ? 'Iniciar Curso' : 'Ver Detalhes' }}
                    <Play class="h-4 w-4" />
                  </router-link>
                </div>
              </div>
            </div>
          </div>
          
          <div
            v-else
            class="text-center py-12"
          >
            <p class="text-gray-600">
              Nenhum curso disponível no momento.
            </p>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.store'; // Para o botão de login/iniciar curso
import homeService from '@/services/homeService';
import {
  BookOpen,
  Guitar,
  GraduationCap,
  Star,
  Clock
} from 'lucide-vue-next'
import { ArrowRight, Play, Heart, Users, Award } from 'lucide-vue-next'
import { useHead } from '@vueuse/head';

useHead({
  title: 'Página Inicial | Som que Conecta',
  meta: [
    { name: 'description', content: 'Página inicial com o conteúdo mais recente da plataforma.' },
  ]
})

// Estado para armazenar os dados vindos da API
const latestArticle = ref(null);
const latestCourse = ref(null);
const isLoading = ref(true);

const authStore = useAuthStore();
const isLoggedIn = ref(authStore.isAuthenticated); // Pega o estado de login

// Funções de formatação (você já as tem)
const formatDate = (dateString) => {
    if (!dateString) return '';
    return new Intl.DateTimeFormat('pt-BR', { day: 'numeric', month: 'long', year: 'numeric' }).format(new Date(dateString));
};

const formatDuration = (time, type) => {
    if (!time || !type) return '';
    const typeMap = { 'D': 'dias', 'M': 'meses', 'Y': 'anos' };
    const plural = time > 1 ? typeMap[type] : typeMap[type].slice(0, -1);
    return `${time} ${plural}`;
};

// Função para buscar os dados
const fetchHomePageData = async () => {
  isLoading.value = true;
  try {
    const [articleResponse, courseResponse] = await homeService.getHomePageData();
    
    // A API retorna uma lista com 1 item, então pegamos o primeiro
    if (articleResponse.data && articleResponse.data.length > 0) {
      latestArticle.value = articleResponse.data[0];
    }
    
    if (courseResponse.data && courseResponse.data.length > 0) {
      latestCourse.value = courseResponse.data[0];
    }
  } catch (error) {
    console.error("Erro ao carregar dados da página inicial:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(fetchHomePageData);

</script>