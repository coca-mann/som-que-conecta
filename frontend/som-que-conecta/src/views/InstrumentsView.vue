<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Instrumentos Disponíveis</h1>
      <p class="text-gray-600">Instrumentos musicais disponibilizados por ONGs e professores independentes</p>
    </div>

    <!-- Filters -->
    <div class="mb-8 flex flex-wrap gap-4">
      <select v-model="selectedType" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option value="">Todos os Tipos</option>
        <option v-for="type in instrumentTypes" :key="type.id" :value="type.name">{{ type.name }}</option>
      </select>
      
      <select v-model="selectedBrand" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option value="">Todas as Marcas</option>
        <option v-for="brand in instrumentBrands" :key="brand.id" :value="brand.name">{{ brand.name }}</option>
      </select>
      
      <div class="flex items-center gap-2">
        <input v-model="showAvailableOnly" type="checkbox" id="available" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
        <label for="available" class="text-sm text-gray-700">Apenas disponíveis</label>
      </div>
    </div>

    <!-- Instruments Grid -->
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="instrument in filteredInstruments" :key="instrument.id" class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow flex flex-col">
        <div class="relative">
          <img :src="instrument.main_image" :alt="instrument.name" class="w-full h-48 object-cover">
          <div class="absolute top-3 right-3">
            <span :class="instrument.is_loanable ? 'bg-green-500' : 'bg-red-500'" class="px-2 py-1 text-white text-xs rounded-full font-medium">
              {{ instrument.is_loanable ? 'Disponível' : 'Indisponível' }}
            </span>
          </div>
        </div>
        
        <div class="p-6 flex flex-col flex-grow">
          <div class="flex items-center justify-between mb-3">
            <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full font-medium">{{ instrument.type_name }}</span>
            <span class="text-sm font-medium text-gray-600">{{ instrument.brand_name }}</span>
          </div>
          
          <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ instrument.name }}</h3>
          
          <div class="space-y-2 mb-4">
            <div class="flex items-center gap-2 text-sm text-gray-600">
              <div class="w-4 h-4 rounded-full border-2 border-gray-300" :style="{ backgroundColor: instrument.color }"></div>
              <span class="capitalize">{{ instrument.color_name }}</span>
            </div>
            <p class="text-gray-600 text-sm leading-relaxed">{{ instrument.description }}</p>
          </div>
          
          <div class="space-y-2 mb-4 pt-4 border-t border-gray-100">
            <div class="flex items-center gap-2 text-sm text-gray-600">
              <User class="h-4 w-4" />
              <span>{{ instrument.provider }}</span>
            </div>
            <template v-if="instrument.is_loanable">
              <div class="flex items-center gap-2 text-sm text-gray-600">
                <MapPin class="h-4 w-4" />
                <span>{{ instrument.location }}</span>
              </div>
              <div class="flex items-center gap-2 text-sm text-gray-600">
                <Clock class="h-4 w-4" />
                <span>{{ instrument.availability }}</span>
              </div>
            </template>
          </div>
          
          <div class="mt-auto pt-4">
            <button 
              @click="requestScheduling(instrument)" 
              :disabled="!instrument.is_loanable || !isAuthenticated"
              :class="[
                'w-full px-4 py-2 rounded-lg transition-colors font-medium',
                instrument.is_loanable && isAuthenticated
                  ? 'bg-blue-600 text-white hover:bg-blue-700' 
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              ]"
            >
              {{ !isAuthenticated ? 'Faça login para agendar' : instrument.is_loanable ? 'Solicitar Agendamento' : 'Indisponível' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Scheduling Modal -->
    <Teleport to="body">
      <SchedulingModal 
        v-if="selectedInstrument" 
        :instrument="selectedInstrument" 
        @close="selectedInstrument = null" 
        @scheduled="handleScheduled" 
      />
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.store';
import instrumentService from '@/services/instrumentService';
import { storeToRefs } from 'pinia';
import { MapPin, User, Clock } from 'lucide-vue-next'
import SchedulingModal from '@/components/modals/SchedulingModal.vue'

const authStore = useAuthStore();
const isLoggedIn = computed(() => !!authStore.user);
const { isAuthenticated } = storeToRefs(authStore);

// ** NOVO: Estado para carregamento e erros **
const instruments = ref([]); // Começa vazio
const isLoading = ref(false);
const error = ref(null);

const selectedType = ref('')
const selectedBrand = ref('')
const showAvailableOnly = ref(false)
const selectedInstrument = ref(null)

// Novos estados para tipos e marcas
const instrumentTypes = ref([])
const instrumentBrands = ref([])

onMounted(async () => {
  console.log('Componente montado. Forçando a chamada da API para teste.');
  await Promise.all([
    fetchInstruments(),
    fetchInstrumentTypes(),
    fetchInstrumentBrands()
  ]);
});

const filteredInstruments = computed(() => {
  let filtered = instruments.value

  if (selectedType.value) {
    filtered = filtered.filter(instrument => 
      instrument.type.toLowerCase().includes(selectedType.value.toLowerCase())
    )
  }

  if (selectedBrand.value) {
    filtered = filtered.filter(instrument =>
      instrument.brand.toLowerCase().includes(selectedBrand.value.toLowerCase())
    )
  }

  if (showAvailableOnly.value) {
    filtered = filtered.filter(instrument => instrument.is_loanable === true)
  }

  return filtered
})

const fetchInstruments = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    const response = await instrumentService.getPublicInstruments();
    instruments.value = response.data;
  } catch (err) {
    console.error("Erro ao buscar instrumentos:", err);
    error.value = err.response?.data?.detail || "Não foi possível conectar ao servidor.";
  } finally {
    isLoading.value = false;
  }
};

const fetchInstrumentTypes = async () => {
  try {
    const response = await instrumentService.getInstrumentTypes();
    instrumentTypes.value = response.data;
  } catch (err) {
    console.error("Erro ao buscar tipos de instrumentos:", err);
  }
};

const fetchInstrumentBrands = async () => {
  try {
    const response = await instrumentService.getInstrumentBrands();
    instrumentBrands.value = response.data;
  } catch (err) {
    console.error("Erro ao buscar marcas de instrumentos:", err);
  }
};

const requestScheduling = (instrument) => {
  console.log('Abrindo modal para:', instrument)
  selectedInstrument.value = instrument
}

const handleScheduled = (schedulingData) => {
  console.log('Agendamento solicitado:', schedulingData)
  selectedInstrument.value = null
}
</script>