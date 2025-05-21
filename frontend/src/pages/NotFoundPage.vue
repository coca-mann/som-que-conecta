<template>
    <div class="text-center py-20">
      <AlertTriangleIcon class="h-24 w-24 text-amber-500 mx-auto mb-6" />
      <h1 class="text-5xl font-bold text-gray-700 mb-4">404</h1>
      <p class="text-2xl text-gray-600 mb-8">Página Não Encontrada</p>
      <p class="text-gray-500 mb-8">
        Desculpe, a página que você está procurando não existe ou foi movida.
      </p>
      <router-link 
        to="/" 
        class="px-6 py-3 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors text-lg"
      >
        Voltar para a Página Inicial
      </router-link>
    </div>
  </template>
  
  <script setup>
  import { AlertTriangleIcon } from 'lucide-vue-next';
  </script>