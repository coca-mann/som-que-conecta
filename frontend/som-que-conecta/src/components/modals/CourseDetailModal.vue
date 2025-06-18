<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 max-w-2xl w-full">
      <h2 class="text-2xl font-bold mb-4">
        {{ course.title }}
      </h2>
      <div class="space-y-4">
        <p class="text-gray-600">
          {{ course.description }}
        </p>
        <div class="flex justify-between items-center">
          <span class="text-lg font-semibold">R$ {{ course.price }}</span>
          <button 
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            @click="handleEnroll"
          >
            Inscrever-se
          </button>
        </div>
      </div>
      <button 
        class="mt-4 px-4 py-2 text-gray-700 hover:text-gray-900"
        @click="$emit('close')"
      >
        Fechar
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  course: {
    type: Object,
    required: true
  }
})

const handleEnroll = () => {
  // Aqui você implementará a lógica para inscrição no curso
  console.log('Inscrição no curso:', props.course)
}

const emit = defineEmits(['close'])
</script> 