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
          <img :src="instrument.image" :alt="instrument.name" class="w-full h-48 object-cover">
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
            <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full font-medium">{{ instrument.type }}</span>
            <span class="text-sm font-medium text-gray-600">{{ instrument.brand }}</span>
          </div>
          
          <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ instrument.name }}</h3>
          
          <div class="space-y-2 mb-4">
            <div class="flex items-center gap-2 text-sm text-gray-600">
              <div class="w-4 h-4 rounded-full border-2 border-gray-300" :style="{ backgroundColor: instrument.color }"></div>
              <span class="capitalize">{{ instrument.colorName }}</span>
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
              <span>{{ instrument.availableHours }}</span>
            </div>
            <div class="flex items-center gap-2 text-sm text-gray-600">
              <Calendar class="h-4 w-4" />
              <span>{{ instrument.bookings }} agendamentos</span>
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
import { ref, computed } from 'vue'
import { Plus, Edit, Trash2, Star, MapPin, Clock, Calendar, AlertTriangle } from 'lucide-vue-next'
import InstrumentFormModal from '../components/modals/InstrumentFormModal.vue'

const selectedType = ref('')
const selectedStatus = ref('')
const showAddModal = ref(false)
const editingInstrument = ref(null)
const instrumentToDelete = ref(null)

const instruments = ref([
  {
    id: 1,
    name: 'Violão Clássico Yamaha C40',
    type: 'Cordas',
    brand: 'Yamaha',
    color: '#8B4513',
    colorName: 'Natural',
    description: 'Violão clássico com tampo em abeto sólido, ideal para iniciantes e estudantes. Possui excelente projeção sonora e acabamento impecável.',
    location: 'Centro - Sala 101',
    availableHours: 'Seg-Sex: 14h-18h',
    status: 'available',
    featured: true,
    bookings: 12,
    image: '/placeholder.svg?height=200&width=300'
  },
  {
    id: 2,
    name: 'Teclado Yamaha PSR-E373',
    type: 'Teclas',
    brand: 'Yamaha',
    color: '#000000',
    colorName: 'Preto',
    description: 'Teclado eletrônico com 61 teclas sensíveis ao toque, 622 vozes de alta qualidade e 205 estilos de acompanhamento.',
    location: 'Zona Norte - Estúdio A',
    availableHours: 'Sáb-Dom: 9h-17h',
    status: 'available',
    featured: false,
    bookings: 8,
    image: '/placeholder.svg?height=200&width=300'
  },
  {
    id: 3,
    name: 'Flauta Transversal Pearl PF-505E',
    type: 'Sopro',
    brand: 'Pearl',
    color: '#C0C0C0',
    colorName: 'Prata',
    description: 'Flauta transversal profissional em prata maciça com chaves abertas. Excelente resposta em todos os registros.',
    location: 'Zona Sul - Conservatório',
    availableHours: 'Ter-Qui: 10h-16h',
    status: 'maintenance',
    featured: false,
    bookings: 5,
    image: '/placeholder.svg?height=200&width=300'
  },
  {
    id: 4,
    name: 'Guitarra Elétrica Fender Stratocaster',
    type: 'Cordas',
    brand: 'Fender',
    color: '#FF0000',
    colorName: 'Vermelho',
    description: 'Guitarra elétrica clássica com corpo em alder, braço em maple e escala em rosewood. Três captadores single-coil.',
    location: 'Zona Oeste - Escola de Rock',
    availableHours: 'Seg-Sex: 19h-22h',
    status: 'available',
    featured: true,
    bookings: 15,
    image: '/placeholder.svg?height=200&width=300'
  },
  {
    id: 5,
    name: 'Bateria Acústica Pearl Export',
    type: 'Percussão',
    brand: 'Pearl',
    color: '#000080',
    colorName: 'Azul',
    description: 'Kit completo de bateria acústica com 5 tambores, caixa, bumbo, dois tons e floor tom. Inclui pratos e acessórios.',
    location: 'Centro - Estúdio de Percussão',
    availableHours: 'Ter-Dom: 10h-20h',
    status: 'available',
    featured: false,
    bookings: 20,
    image: '/placeholder.svg?height=200&width=300'
  }
])

const filteredInstruments = computed(() => {
  let filtered = instruments.value

  if (selectedType.value) {
    filtered = filtered.filter(instrument => 
      instrument.type.toLowerCase().includes(selectedType.value.toLowerCase())
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

const closeModal = () => {
  showAddModal.value = false
  editingInstrument.value = null
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
}
</script>