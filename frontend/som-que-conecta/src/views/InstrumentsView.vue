<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">
        Instrumentos Disponíveis
      </h1>
      <p class="text-gray-600">
        Instrumentos musicais disponibilizados por ONGs e professores independentes
      </p>
    </div>

    <div
      v-if="!isAuthenticated"
      class="mb-8 bg-red-50 border border-red-200 rounded-lg p-6 text-center"
    >
      <h2 class="text-xl font-semibold text-red-900 mb-2">
        Faça login para acessar os instrumentos
      </h2>
      <p class="text-red-700 mb-4">
        Para solicitar o empréstimo de instrumentos, você precisa estar logado em sua conta.
      </p>
      <router-link 
        to="/auth?redirect=/instruments" 
        class="inline-flex items-center px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
      >
        Fazer Login
      </router-link>
    </div>

    <div
      v-if="isAuthenticated"
      class="mb-8 flex flex-wrap gap-4"
    >
      <select
        v-model="selectedType"
        class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
      >
        <option value="">
          Todos os Tipos
        </option>
        <option
          v-for="type in instrumentTypes"
          :key="type.id"
          :value="type.name"
        >
          {{ type.name }}
        </option>
      </select>
      
      <select
        v-model="selectedBrand"
        class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
      >
        <option value="">
          Todas as Marcas
        </option>
        <option
          v-for="brand in instrumentBrands"
          :key="brand.id"
          :value="brand.name"
        >
          {{ brand.name }}
        </option>
      </select>
      
      <div class="flex items-center gap-2">
        <input
          id="available"
          v-model="showAvailableOnly"
          type="checkbox"
          class="rounded border-gray-300 text-red-600 focus:ring-red-500"
        >
        <label
          for="available"
          class="text-sm text-gray-700"
        >Apenas disponíveis</label>
      </div>
    </div>

    <div
      v-if="isAuthenticated"
      class="grid md:grid-cols-2 lg:grid-cols-3 gap-6"
    >
      <div
        v-for="instrument in filteredInstruments"
        :key="instrument.id"
        class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow flex flex-col"
      >
        <div class="relative">
          <div class="relative w-full h-48 overflow-hidden">
            <div
              class="flex transition-transform duration-300 ease-in-out"
              :style="{ transform: `translateX(-${currentImageIndex[instrument.id] * 100}%)` }"
            >
              <img 
                v-for="(image, index) in instrument.images" 
                :key="image.id"
                :src="image.picture" 
                :alt="`${instrument.name} - Imagem ${index + 1}`"
                class="w-full h-48 object-cover flex-shrink-0"
              >
            </div>
            
            <div
              v-if="instrument.images.length > 1"
              class="absolute inset-0 flex items-center"
            >
              <div class="absolute left-2">
                <button 
                  v-show="currentImageIndex[instrument.id] > 0"
                  class="rounded-full p-1 text-white transition-all duration-200 bg-black/20 hover:bg-black/40"
                  @click.stop="previousImage(instrument.id)"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M15 19l-7-7 7-7"
                    />
                  </svg>
                </button>
              </div>
              <div class="absolute right-2">
                <button 
                  v-show="currentImageIndex[instrument.id] < instrument.images.length - 1"
                  class="rounded-full p-1 text-white transition-all duration-200 bg-black/20 hover:bg-black/40"
                  @click.stop="nextImage(instrument.id)"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9 5l7 7-7 7"
                    />
                  </svg>
                </button>
              </div>
            </div>
            
            <div
              v-if="instrument.images.length > 1"
              class="absolute bottom-2 left-0 right-0 flex justify-center gap-1"
            >
              <button 
                v-for="(_, index) in instrument.images" 
                :key="index"
                class="w-2 h-2 rounded-full transition-colors"
                :class="currentImageIndex[instrument.id] === index ? 'bg-white' : 'bg-white bg-opacity-50'"
                @click.stop="currentImageIndex[instrument.id] = index"
              />
            </div>
          </div>
          <div class="absolute top-3 right-3">
            <span
              :class="instrument.is_loanable ? 'bg-green-500' : 'bg-red-500'"
              class="px-2 py-1 text-white text-xs rounded-full font-medium"
            >
              {{ instrument.is_loanable ? 'Disponível' : 'Indisponível' }}
            </span>
          </div>
        </div>
        
        <div class="p-6 flex flex-col flex-grow">
          <div class="flex items-center justify-between mb-3">
            <span class="px-2 py-1 bg-red-100 text-red-800 text-xs rounded-full font-medium">{{ instrument.type_name }}</span>
            <span class="text-sm font-medium text-gray-600">{{ instrument.brand_name }}</span>
          </div>
          
          <h3 class="text-xl font-semibold text-gray-900 mb-2">
            {{ instrument.name }}
          </h3>
          
          <div class="space-y-2 mb-4">
            <div class="flex items-center gap-2 text-sm text-gray-600">
              <div
                class="w-4 h-4 rounded-full border-2 border-gray-300"
                :style="{ backgroundColor: instrument.color }"
              />
              <span class="capitalize">{{ instrument.color_name }}</span>
            </div>
            <p class="text-gray-600 text-sm leading-relaxed">
              {{ instrument.description }}
            </p>
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
              :disabled="!instrument.is_loanable || !isAuthenticated" 
              :class="[
                'w-full px-4 py-2 rounded-lg transition-colors font-medium',
                instrument.is_loanable && isAuthenticated
                  ? 'bg-red-600 text-white hover:bg-red-700' 
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              ]"
              @click="requestScheduling(instrument)"
            >
              {{ !isAuthenticated ? 'Faça login para agendar' : instrument.is_loanable ? 'Solicitar Agendamento' : 'Indisponível' }}
            </button>
          </div>
        </div>
      </div>
    </div>

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
import { ref, computed, onMounted, watch } from 'vue'
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

// Estado para controlar o índice da imagem atual de cada instrumento
const currentImageIndex = ref({})

// Watcher para carregar dados quando o usuário fizer login
watch(isAuthenticated, async (newValue) => {
  if (newValue) {
    console.log('Usuário autenticado. Carregando dados dos instrumentos.');
    await Promise.all([
      fetchInstruments(),
      fetchInstrumentTypes(),
      fetchInstrumentBrands()
    ]);
  }
});

onMounted(async () => {
  if (isAuthenticated.value) {
    console.log('Usuário autenticado. Carregando dados dos instrumentos.');
    await Promise.all([
      fetchInstruments(),
      fetchInstrumentTypes(),
      fetchInstrumentBrands()
    ]);
  }
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
    // Inicializar o índice de imagens para cada instrumento
    instruments.value.forEach(instrument => {
      currentImageIndex.value[instrument.id] = 0
    })
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

// Funções para controlar o carrossel
const nextImage = (instrumentId) => {
  if (!currentImageIndex.value[instrumentId]) {
    currentImageIndex.value[instrumentId] = 0
  }
  const instrument = instruments.value.find(i => i.id === instrumentId)
  if (currentImageIndex.value[instrumentId] < instrument.images.length - 1) {
    currentImageIndex.value[instrumentId]++
  }
}

const previousImage = (instrumentId) => {
  if (currentImageIndex.value[instrumentId] > 0) {
    currentImageIndex.value[instrumentId]--
  }
}
</script>