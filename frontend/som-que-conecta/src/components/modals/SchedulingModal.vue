<template>
  <div class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold text-gray-900">Agendar Aula</h2>
        <button 
          @click="$emit('close')"
          class="text-gray-400 hover:text-gray-500"
        >
          <X class="h-6 w-6" />
        </button>
      </div>

      <div class="mb-6 p-4 bg-gray-50 rounded-lg">
        <h3 class="font-semibold text-gray-900 mb-2">{{ instrument.name }}</h3>
        <div class="flex items-center gap-2 text-sm text-gray-600">
          <MapPin class="h-4 w-4" />
          <span>{{ instrument.location }}</span>
        </div>
        <div class="flex items-center gap-2 text-sm text-gray-600 mt-1">
          <Clock class="h-4 w-4" />
          <span>{{ instrument.availableHours }}</span>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Data</label>
          <input 
            v-model="date"
            type="date"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          >
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Horário</label>
          <input 
            v-model="time"
            type="time"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            required
          >
        </div>
        <div class="flex justify-end space-x-2 mt-6">
          <button 
            type="button"
            class="px-4 py-2 text-gray-700 hover:text-gray-900"
            @click="$emit('close')"
          >
            Cancelar
          </button>
          <button 
            type="submit"
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Agendar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { MapPin, Clock, X } from 'lucide-vue-next'

const props = defineProps({
  instrument: {
    type: Object,
    required: true
  }
})

const date = ref('')
const time = ref('')

const handleSubmit = () => {
  const schedulingData = {
    instrumentId: props.instrument.id,
    instrumentName: props.instrument.name,
    date: date.value,
    time: time.value
  }
  emit('scheduled', schedulingData)
}

const emit = defineEmits(['close', 'scheduled'])
</script> 