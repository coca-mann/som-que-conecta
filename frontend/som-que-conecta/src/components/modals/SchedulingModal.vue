<template>
  <div class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-bold text-gray-900">
          Agendar Aula
        </h2>
        <button 
          class="text-gray-400 hover:text-gray-500"
          @click="$emit('close')"
        >
          <X class="h-6 w-6" />
        </button>
      </div>

      <div class="mb-6 p-4 bg-gray-50 rounded-lg">
        <h3 class="font-semibold text-gray-900 mb-2">
          {{ instrument.name }}
        </h3>
        <div class="flex items-center gap-2 text-sm text-gray-600">
          <MapPin class="h-4 w-4" />
          <span>{{ instrument.location }}</span>
        </div>
        <div class="flex items-center gap-2 text-sm text-gray-600 mt-1">
          <Clock class="h-4 w-4" />
          <span>{{ instrument.availableHours }}</span>
        </div>
      </div>

      <div
        v-if="error"
        class="mb-4 p-3 bg-red-100 text-red-700 rounded-md text-sm"
      >
        <p><b>Erro ao agendar:</b></p>
        <p>{{ error }}</p>
      </div>

      <form
        class="space-y-4"
        @submit.prevent="handleSubmit"
      >
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
          <label class="block text-sm font-medium text-gray-700">Horário Início</label>
          <div class="flex gap-2">
            <select 
              v-model="startHour"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            >
              <option
                v-for="hour in hours"
                :key="hour"
                :value="hour"
              >
                {{ hour.toString().padStart(2, '0') }}h
              </option>
            </select>
            <select 
              v-model="startMinute"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            >
              <option
                v-for="minute in minutes"
                :key="minute"
                :value="minute"
              >
                {{ minute.toString().padStart(2, '0') }}min
              </option>
            </select>
          </div>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Horário Fim</label>
          <div class="flex gap-2">
            <select 
              v-model="endHour"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            >
              <option
                v-for="hour in hours"
                :key="hour"
                :value="hour"
              >
                {{ hour.toString().padStart(2, '0') }}h
              </option>
            </select>
            <select 
              v-model="endMinute"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            >
              <option
                v-for="minute in minutes"
                :key="minute"
                :value="minute"
              >
                {{ minute.toString().padStart(2, '0') }}min
              </option>
            </select>
          </div>
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
            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Agendando...' : 'Agendar' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { MapPin, Clock, X } from 'lucide-vue-next'
import instrumentService from '@/services/instrumentService'

const props = defineProps({
  instrument: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'scheduled'])

const date = ref('')
const startHour = ref('09')
const startMinute = ref('00')
const endHour = ref('10')
const endMinute = ref('00')
const isLoading = ref(false)
const error = ref(null)

// Arrays para as opções de horas e minutos
const hours = Array.from({ length: 24 }, (_, i) => i.toString().padStart(2, '0'))
const minutes = Array.from({ length: 12 }, (_, i) => (i * 5).toString().padStart(2, '0'))

// Computed properties para formatar os horários
const startTime = computed(() => `${startHour.value}:${startMinute.value}`)
const endTime = computed(() => `${endHour.value}:${endMinute.value}`)

const handleSubmit = async () => {
  isLoading.value = true;
  error.value = null;

  const payload = {
    instrument_id: props.instrument.id,
    reservation_date: date.value,
    reservation_starttime: startTime.value,
    reservation_endtime: endTime.value,
  };

  try {
    const response = await instrumentService.createBooking(payload);
    emit('scheduled', response.data);
    emit('close');
  } catch (err) {
    const apiError = err.response?.data;
    
    // LÓGICA DE ERRO ATUALIZADA
    if (apiError && typeof apiError === 'object') {
      // Se o erro for um objeto, formata as mensagens
      let errorMessages = [];
      for (const [key, value] of Object.entries(apiError)) {
        if (Array.isArray(value)) {
          // Se o valor for um array, junta as mensagens (comportamento esperado do DRF)
          errorMessages.push(`${key}: ${value.join(', ')}`);
        } else {
          // Se não for um array (como o erro 405), apenas mostra o valor
          errorMessages.push(`${value}`);
        }
      }
      error.value = errorMessages.join('; ');
    } else if (apiError) {
      // Se o erro for um texto simples
      error.value = apiError;
    } else {
      error.value = "Ocorreu um erro inesperado. Tente novamente.";
    }
    console.error("Erro no agendamento:", err.response?.data || err.message);
  } finally {
    isLoading.value = false;
  }
}
</script> 