<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Gerenciar Instrumentos</h1>
        <p class="text-gray-600">Gerencie os instrumentos disponíveis para empréstimo</p>
      </div>
      
      <button @click="showAddModal = true" class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2">
        <Plus class="h-5 w-5" />
        Adicionar Instrumento
      </button>
    </div>

    <!-- Filters -->
    <div class="mb-8 flex flex-wrap gap-4">
      <select v-model="selectedType" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option value="">Todos os Tipos</option>
        <option value="cordas">Cordas</option>
        <option value="sopro">Sopro</option>
        <option value="percussao">Percussão</option>
        <option value="teclas">Teclas</option>
      </select>
      
      <select v-model="selectedStatus" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option value="">Todos os Status</option>
        <option value="available">Disponível</option>
        <option value="unavailable">Indisponível</option>
        <option value="maintenance">Em Manutenção</option>
      </select>
    </div>

    <!-- Instruments Grid -->
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="instrument in filteredInstruments" :key="instrument.id" class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
        <div class="relative">
          <img :src="instrument.main_image || '/placeholder.svg'" :alt="instrument.name" class="w-full h-48 object-cover">
          <div class="absolute top-3 right-3">
            <span :class="getStatusColor(instrument.status)" class="px-2 py-1 text-white text-xs rounded-full font-medium">
              {{ getStatusLabel(instrument.status) }}
            </span>
          </div>
          <div class="absolute top-3 left-3">
            <button @click="toggleFeatured(instrument)" :class="[
              'p-2 rounded-full transition-colors',
              instrument.featured ? 'bg-yellow-500 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'
            ]">
              <Star :class="instrument.featured ? 'fill-current' : ''" class="h-4 w-4" />
            </button>
          </div>
        </div>
        
        <div class="p-6">
          <div class="flex items-center justify-between mb-3">
            <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full font-medium">{{ instrument.type_name }}</span>
            <span class="text-sm font-medium text-gray-600">{{ instrument.brand_name }}</span>
          </div>
          
          <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ instrument.name }}</h3>
          
          <div class="space-y-2 mb-4">
            <div class="flex items-center gap-2 text-sm text-gray-600">
              <div class="w-4 h-4 rounded-full border-2 border-gray-300" :style="{ backgroundColor: instrument.color }"></div>
              <span class="capitalize">{{ instrument.color }}</span>
            </div>
            <p class="text-gray-600 text-sm leading-relaxed">{{ instrument.description }}</p>
          </div>
          
          <div class="space-y-2 mb-4 pt-4 border-t border-gray-100">
            <div class="flex items-center gap-2 text-sm text-gray-600">
              <MapPin class="h-4 w-4" />
              <span>{{ instrument.location }}</span>
            </div>
            <div class="flex items-center gap-2 text-sm text-gray-600">
              <Clock class="h-4 w-4" />
              <span>{{ instrument.availability }}</span>
            </div>
            <div class="flex items-center gap-2 text-sm text-gray-600">
              <Calendar class="h-4 w-4" />
              <span>{{ instrument.bookings_count }} agendamentos</span>
            </div>
          </div>
          
          <div class="flex gap-2">
            <button @click="editInstrument(instrument)" class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm">
              <Edit class="h-4 w-4 inline mr-1" />
              Editar
            </button>
            <button @click="toggleAvailability(instrument)" :class="[
              'flex-1 px-4 py-2 rounded-lg transition-colors text-sm',
              instrument.status === 'available' 
                ? 'bg-red-100 text-red-700 hover:bg-red-200' 
                : 'bg-green-100 text-green-700 hover:bg-green-200'
            ]">
              {{ instrument.status === 'available' ? 'Desativar' : 'Ativar' }}
            </button>
            <button @click="deleteInstrument(instrument)" class="px-3 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors">
              <Trash2 class="h-4 w-4" />
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Instrument Modal -->
    <InstrumentFormModal 
      v-if="showAddModal || editingInstrument" 
      :instrument="editingInstrument"
      @close="closeModal" 
      @saved="handleInstrumentSaved" 
    />

    <!-- Delete Confirmation Modal -->
    <div v-if="instrumentToDelete" class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <div class="text-center">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <AlertTriangle class="h-8 w-8 text-red-600" />
          </div>
          <h3 class="text-lg font-semibold mb-2">Confirmar Exclusão</h3>
          <p class="text-gray-600 mb-6">
            Tem certeza que deseja excluir o instrumento "{{ instrumentToDelete.name }}"? 
            Esta ação não pode ser desfeita.
          </p>
          <div class="flex gap-3 justify-center">
            <button @click="instrumentToDelete = null" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
              Cancelar
            </button>
            <button @click="confirmDelete" class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors">
              Excluir
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.store'
import { Plus, Edit, Trash2, Star, MapPin, Clock, Calendar, AlertTriangle } from 'lucide-vue-next'
import InstrumentFormModal from '../components/modals/InstrumentFormModal.vue'
import instrumentService from '@/services/instrumentService'

const authStore = useAuthStore()

const selectedType = ref('')
const selectedStatus = ref('')
const showAddModal = ref(false)
const editingInstrument = ref(null)
const instrumentToDelete = ref(null)

const canManageDetails = computed(() => authStore.canManageInstrumentDetails)

// --- 2. Refs para controlar o estado ---
const instruments = ref([]) // Começa vazio, será preenchido pela API
const isLoading = ref(false) // Para mostrar um feedback de carregamento (ex: um spinner)
const error = ref(null) // Para guardar mensagens de erro

// --- 3. A função para buscar os dados ---
const fetchInstruments = async () => {
  isLoading.value = true
  error.value = null
  try {
    const response = await instrumentService.getInstruments()
    instruments.value = response.data
    console.log('Instrumentos carregados da API:', response.data)
  } catch (err) {
    console.error("Erro ao buscar instrumentos:", err)
    error.value = "Não foi possível carregar os instrumentos. Tente novamente mais tarde."
  } finally {
    isLoading.value = false
  }
}

// --- 4. Chamar a função quando o componente for montado ---
onMounted(() => {
  fetchInstruments()
})

const filteredInstruments = computed(() => {
  // A lógica de filtro continua funcionando normalmente!
  let filtered = instruments.value

  if (selectedType.value) {
    // Ajuste aqui para usar 'type_name' que vem da API
    filtered = filtered.filter(instrument =>
      instrument.type_name.toLowerCase().includes(selectedType.value.toLowerCase())
    )
  }

  if (selectedStatus.value) {
    filtered = filtered.filter(instrument => instrument.status === selectedStatus.value)
  }

  return filtered
})

const getStatusColor = (status) => {
  const colors = {
    available: 'bg-green-500',
    unavailable: 'bg-red-500',
    maintenance: 'bg-yellow-500'
  }
  return colors[status] || 'bg-gray-500'
}

const getStatusLabel = (status) => {
  const labels = {
    available: 'Disponível',
    unavailable: 'Indisponível',
    maintenance: 'Manutenção'
  }
  return labels[status] || 'Desconhecido'
}

const toggleFeatured = (instrument) => {
  instrument.featured = !instrument.featured
  console.log('Featured toggled:', instrument.id, instrument.featured)
}

const editInstrument = (instrument) => {
  editingInstrument.value = { ...instrument }
}

const toggleAvailability = (instrument) => {
  instrument.status = instrument.status === 'available' ? 'unavailable' : 'available'
  console.log('Availability toggled:', instrument.id, instrument.status)
}

const deleteInstrument = (instrument) => {
  instrumentToDelete.value = instrument
}

const confirmDelete = () => {
  const index = instruments.value.findIndex(i => i.id === instrumentToDelete.value.id)
  if (index !== -1) {
    instruments.value.splice(index, 1)
  }
  instrumentToDelete.value = null
  console.log('Instrument deleted')
}

const handleInstrumentSaved = (instrumentData) => {
  if (editingInstrument.value) {
    // Update existing instrument
    const index = instruments.value.findIndex(i => i.id === editingInstrument.value.id)
    if (index !== -1) {
      instruments.value[index] = { ...instrumentData, id: editingInstrument.value.id }
    }
  } else {
    // Add new instrument
    instruments.value.push({
      ...instrumentData,
      id: Date.now(),
      status: 'available',
      featured: false,
      bookings: 0
    })
  }
  closeModal()
  fetchInstruments();
}

const closeModal = () => {
  showAddModal.value = false
  editingInstrument.value = null
}

</script>