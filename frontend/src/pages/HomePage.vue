<template>
    <div class="space-y-8">
      <section class="text-center py-12">
        <h1 class="text-4xl md:text-5xl font-bold text-emerald-800 mb-4">Aprenda Música no Seu Ritmo</h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto">
          Descubra o mundo dos instrumentos musicais e desenvolva suas habilidades com nossos cursos e recursos.
        </p>
        <router-link
          to="/cursos"
          class="mt-6 inline-block px-6 py-3 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors"
        >
          Explorar Cursos
        </router-link>
      </section>
  
      <section class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white rounded-lg shadow-md overflow-hidden">
          <div class="h-48 bg-emerald-200 flex items-center justify-center">
            <BookOpenIcon class="h-16 w-16 text-emerald-700" />
          </div>
          <div class="p-4">
            <h3 class="text-xl font-semibold mb-2">Artigos Públicos</h3>
            <p class="text-gray-600 mb-4">Confira nossos artigos sobre teoria musical e técnicas de aprendizado.</p>
            <router-link to="/artigos" class="text-emerald-600 hover:text-emerald-500">
              Ver Artigos →
            </router-link>
          </div>
        </div>
  
        <div class="bg-white rounded-lg shadow-md overflow-hidden">
          <div class="h-48 bg-amber-200 flex items-center justify-center">
            <MusicIcon class="h-16 w-16 text-amber-700" />
          </div>
          <div class="p-4">
            <h3 class="text-xl font-semibold mb-2">Instrumentos Musicais</h3>
            <p class="text-gray-600 mb-4">Explore nossa coleção de instrumentos disponíveis para aprendizado.</p>
            <router-link to="/instrumentos" class="text-emerald-600 hover:text-emerald-500">
              Ver Instrumentos →
            </router-link>
          </div>
        </div>
  
        <div class="bg-white rounded-lg shadow-md overflow-hidden">
          <div class="h-48 bg-rose-200 flex items-center justify-center">
            <GraduationCapIcon class="h-16 w-16 text-rose-700" />
          </div>
          <div class="p-4">
            <h3 class="text-xl font-semibold mb-2">Mini-Cursos</h3>
            <p class="text-gray-600 mb-4">Comece a aprender com nossos mini-cursos para iniciantes.</p>
            <router-link to="/cursos" class="text-emerald-600 hover:text-emerald-500">
              Ver Cursos →
            </router-link>
          </div>
        </div>
      </section>
  
      <section class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-2xl font-bold mb-4">Atualizações Recentes</h2>
        <div class="space-y-4">
          <div v-for="(update, index) in recentUpdates" :key="index" class="border-b pb-4 last:border-0">
            <div class="flex items-start">
              <div class="bg-emerald-100 p-2 rounded-md mr-4">
                <component :is="update.icon" class="h-5 w-5 text-emerald-600" />
              </div>
              <div>
                <h3 class="font-semibold">{{ update.title }}</h3>
                <p class="text-gray-600">{{ update.description }}</p>
                <span class="text-sm text-gray-500">{{ update.date }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { 
    Music as MusicIcon, 
    BookOpen as BookOpenIcon,
    GraduationCap as GraduationCapIcon,
    FileText as FileTextIcon, // Para recentUpdates
    Guitar as GuitarIcon // Para recentUpdates
  } from 'lucide-vue-next';
  
  // Dados que eram globais, agora são locais para esta página
  const recentUpdates = ref([
    { 
      title: 'Novo Curso de Violão', 
      description: 'Aprenda os fundamentos do violão em nosso novo curso para iniciantes.',
      date: '2 dias atrás',
      icon: GuitarIcon // Usando o ícone importado
    },
    { 
      title: 'Artigo: Teoria Musical Básica', 
      description: 'Um guia completo sobre os fundamentos da teoria musical para iniciantes.',
      date: '5 dias atrás',
      icon: FileTextIcon // Usando o ícone importado
    },
    { 
      title: 'Parceria com ONGs', 
      description: 'Agora temos mais instrumentos disponíveis através de nossas parcerias com ONGs.',
      date: '1 semana atrás',
      icon: MusicIcon // Usando o ícone importado
    }
  ]);
  </script>