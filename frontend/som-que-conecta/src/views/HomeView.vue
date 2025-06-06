<template>
  <main>
    <!-- Hero Section -->
    <section class="relative py-24 bg-gray-50 overflow-hidden">
      <div class="absolute inset-0">
        <img
          src="/hero-pattern.svg"
          alt="Background Pattern"
          class="w-full h-full object-cover opacity-20"
        />
      </div>
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
              class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              Começar Agora
            </router-link>
            <router-link
              to="/articles"
              class="inline-flex items-center justify-center px-5 py-3 text-base font-medium rounded-md text-blue-700 bg-blue-100 hover:bg-blue-200"
            >
              Ler Artigos
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-16 bg-white">
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
            <BookOpen class="h-12 w-12 text-blue-600 mx-auto mb-4" />
            <h3 class="text-xl font-semibold mb-2">Artigos Especializados</h3>
            <p class="text-gray-600">
              Conteúdo criado por professores experientes para guiar seu aprendizado
            </p>
          </div>
          
          <div class="text-center p-6 rounded-lg border border-gray-200 hover:shadow-lg transition-shadow">
            <Guitar class="h-12 w-12 text-blue-600 mx-auto mb-4" />
            <h3 class="text-xl font-semibold mb-2">Instrumentos Disponíveis</h3>
            <p class="text-gray-600">
              Acesse instrumentos musicais disponibilizados por ONGs e professores
            </p>
          </div>
          
          <div class="text-center p-6 rounded-lg border border-gray-200 hover:shadow-lg transition-shadow">
            <GraduationCap class="h-12 w-12 text-blue-600 mx-auto mb-4" />
            <h3 class="text-xl font-semibold mb-2">Minicursos Práticos</h3>
            <p class="text-gray-600">
              Aprenda passo a passo com cursos estruturados e acompanhe seu progresso
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Latest Article Section -->
    <section class="py-16 bg-gradient-to-br from-blue-50 to-indigo-100">
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
          <div class="bg-white rounded-2xl shadow-xl overflow-hidden hover:shadow-2xl transition-shadow duration-300">
            <div class="md:flex">
              <div class="md:w-1/2">
                <img :src="latestArticle.image" :alt="latestArticle.title" class="w-full h-64 md:h-full object-cover">
              </div>
              <div class="md:w-1/2 p-8">
                <div class="flex items-center gap-3 mb-4">
                  <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full font-medium">
                    {{ latestArticle.category }}
                  </span>
                  <div class="flex items-center text-yellow-500">
                    <Star class="h-4 w-4 fill-current" />
                    <span class="text-sm text-gray-600 ml-1">{{ latestArticle.rating }}</span>
                  </div>
                  <span class="text-sm text-gray-500">{{ formatDate(latestArticle.publishedAt) }}</span>
                </div>
                
                <h3 class="text-2xl font-bold text-gray-900 mb-4">{{ latestArticle.title }}</h3>
                <p class="text-gray-600 mb-6 leading-relaxed">{{ latestArticle.excerpt }}</p>
                
                <div class="flex items-center justify-between mb-6">
                  <div class="flex items-center gap-3">
                    <img :src="latestArticle.authorAvatar" :alt="latestArticle.author" class="w-10 h-10 rounded-full">
                    <div>
                      <p class="font-medium text-gray-900">{{ latestArticle.author }}</p>
                      <p class="text-sm text-gray-500">{{ latestArticle.authorRole }}</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-2 text-sm text-gray-500">
                    <Clock class="h-4 w-4" />
                    <span>{{ latestArticle.readTime }} min</span>
                  </div>
                </div>
                
                <router-link to="/articles" class="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium">
                  Ler Artigo Completo
                  <ArrowRight class="h-4 w-4" />
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Latest Course Section -->
    <section class="py-16 bg-gradient-to-br from-purple-50 to-pink-100">
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
          <div class="bg-white rounded-2xl shadow-xl overflow-hidden hover:shadow-2xl transition-shadow duration-300">
            <div class="md:flex md:flex-row-reverse">
              <div class="md:w-1/2">
                <img :src="latestCourse.image" :alt="latestCourse.title" class="w-full h-64 md:h-full object-cover">
              </div>
              <div class="md:w-1/2 p-8">
                <div class="flex items-center gap-3 mb-4">
                  <span class="px-3 py-1 bg-purple-100 text-purple-800 text-sm rounded-full font-medium">
                    {{ latestCourse.level }}
                  </span>
                  <span class="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full font-medium">
                    {{ latestCourse.instrument }}
                  </span>
                  <span class="text-sm text-gray-500">Novo!</span>
                </div>
                
                <h3 class="text-2xl font-bold text-gray-900 mb-4">{{ latestCourse.title }}</h3>
                <p class="text-gray-600 mb-6 leading-relaxed">{{ latestCourse.description }}</p>
                
                <div class="grid grid-cols-2 gap-4 mb-6">
                  <div class="flex items-center gap-2 text-sm text-gray-600">
                    <Clock class="h-4 w-4 text-purple-600" />
                    <span>{{ latestCourse.duration }}</span>
                  </div>
                  <div class="flex items-center gap-2 text-sm text-gray-600">
                    <BookOpen class="h-4 w-4 text-purple-600" />
                    <span>{{ latestCourse.lessons }} aulas</span>
                  </div>
                  <div class="flex items-center gap-2 text-sm text-gray-600">
                    <Users class="h-4 w-4 text-purple-600" />
                    <span>{{ latestCourse.students }} alunos</span>
                  </div>
                  <div class="flex items-center gap-2 text-sm text-gray-600">
                    <Award class="h-4 w-4 text-purple-600" />
                    <span>Certificado</span>
                  </div>
                </div>
                
                <div class="flex items-center gap-3 mb-6">
                  <img :src="latestCourse.instructorAvatar" :alt="latestCourse.instructor" class="w-10 h-10 rounded-full">
                  <div>
                    <p class="font-medium text-gray-900">{{ latestCourse.instructor }}</p>
                    <p class="text-sm text-gray-500">Instrutor Especialista</p>
                  </div>
                </div>
                
                <div class="flex gap-3">
                  <router-link to="/courses" class="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors font-medium">
                    {{ isLoggedIn ? 'Iniciar Curso' : 'Ver Detalhes' }}
                    <Play class="h-4 w-4" />
                  </router-link>
                  <button class="px-4 py-3 border border-purple-600 text-purple-600 rounded-lg hover:bg-purple-50 transition-colors">
                    <Heart class="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import {
  BookOpen,
  Guitar,
  GraduationCap,
  Star,
  Clock
} from 'lucide-vue-next'
import { ArrowRight, Play, Heart, Users, Award } from 'lucide-vue-next'

const latestArticle = ref({
  id: 1,
  title: 'Como Escolher Seu Primeiro Instrumento Musical',
  excerpt: 'Descubra os fatores essenciais para escolher o instrumento ideal para começar sua jornada musical. Considerações sobre orçamento, estilo musical preferido e facilidade de aprendizado.',
  category: 'Iniciantes',
  author: 'Ana Carolina',
  authorRole: 'Professora de Música',
  authorAvatar: '/placeholder.svg?height=40&width=40',
  rating: 4.9,
  readTime: 8,
  publishedAt: new Date('2024-01-20'),
  image: '/placeholder.svg?height=300&width=400'
})

const latestCourse = ref({
  id: 3,
  title: 'Ukulele para Iniciantes Absolutos',
  description: 'Aprenda a tocar ukulele do zero! Este curso foi desenvolvido especialmente para quem nunca tocou um instrumento musical antes. Começamos com o básico e evoluímos gradualmente.',
  level: 'Iniciante',
  instrument: 'Ukulele',
  duration: '3 semanas',
  lessons: 15,
  students: 127,
  instructor: 'Pedro Oliveira',
  instructorAvatar: '/placeholder.svg?height=40&width=40',
  image: '/placeholder.svg?height=300&width=400'
})

const formatDate = (date) => {
  return new Intl.DateTimeFormat('pt-BR', { 
    day: 'numeric', 
    month: 'long', 
    year: 'numeric' 
  }).format(date)
}

const isLoggedIn = ref(false)
</script>