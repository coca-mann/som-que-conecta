<template>
    <div class="space-y-6">
      <h1 class="text-3xl font-bold text-emerald-800 mb-6">Artigos sobre Música</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div v-for="(article, index) in articles" :key="index" class="bg-white rounded-lg shadow-md overflow-hidden">
          <div class="h-48 bg-gradient-to-r from-emerald-400 to-teal-500 flex items-center justify-center">
            <component :is="article.icon" class="h-16 w-16 text-white" />
          </div>
          <div class="p-4">
            <span class="inline-block px-2 py-1 bg-emerald-100 text-emerald-800 rounded-md text-sm mb-2">{{ article.category }}</span>
            <h3 class="text-xl font-semibold mb-2">{{ article.title }}</h3>
            <p class="text-gray-600 mb-4">{{ article.excerpt }}</p>
            <div class="flex justify-between items-center">
              <span class="text-sm text-gray-500">{{ article.date }}</span>
              <button class="text-emerald-600 hover:text-emerald-500">Ler mais →</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { 
    Music as MusicIcon,
    FileText as FileTextIcon,
    Video as VideoIcon,
    Headphones as HeadphonesIcon
  } from 'lucide-vue-next';
  
  const articles = ref([
    {
      title: 'Como Escolher Seu Primeiro Instrumento',
      excerpt: 'Um guia completo para ajudar iniciantes a escolher o instrumento ideal para começar sua jornada musical.',
      category: 'Guia',
      date: '15 de Maio, 2024', // Atualize as datas se necessário
      icon: MusicIcon
    },
    {
      title: 'Fundamentos da Teoria Musical',
      excerpt: 'Entenda os conceitos básicos da teoria musical que todo músico iniciante deve conhecer.',
      category: 'Teoria',
      date: '10 de Maio, 2024',
      icon: FileTextIcon
    },
    {
      title: 'Técnicas de Prática Eficiente',
      excerpt: 'Aprenda como maximizar seu tempo de prática e evoluir mais rapidamente em seu instrumento.',
      category: 'Prática',
      date: '5 de Maio, 2024',
      icon: HeadphonesIcon
    },
    {
      title: 'História do Jazz',
      excerpt: 'Uma jornada pela história do jazz e como ele influenciou a música moderna.',
      category: 'História',
      date: '1 de Maio, 2024',
      icon: VideoIcon
    }
  ]);
  </script>