<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 max-w-2xl w-full">
      <h2 class="text-2xl font-bold mb-4">
        {{ article.title }}
      </h2>
      <p class="text-gray-600 mb-4">
        {{ article.content }}
      </p>
      <button 
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        @click="$emit('close')"
      >
        Fechar
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  article: {
    type: Object,
    required: true
  }
})

defineEmits(['close'])
</script> 