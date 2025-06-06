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
        <option value="cordas">Cordas</option>
        <option value="sopro">Sopro</option>
        <option value="percussao">Percussão</option>
        <option value="teclas">Teclas</option>
      </select>
      
      <select v-model="selectedBrand" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option value="">Todas as Marcas</option>
        <option value="yamaha">Yamaha</option>
        <option value="fender">Fender</option>
        <option value="casio">Casio</option>
        <option value="pearl">Pearl</option>
        <option value="gibson">Gibson</option>
      </select>
      
      <select v-model="selectedLocation" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option value="">Todas as Localizações</option>
        <option value="centro">Centro</option>
        <option value="zona-norte">Zona Norte</option>
        <option value="zona-sul">Zona Sul</option>
        <option value="zona-leste">Zona Leste</option>
        <option value="zona-oeste">Zona Oeste</option>
      </select>
      
      <div class="flex items-center gap-2">
        <input v-model="showAvailableOnly" type="checkbox" id="available" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
        <label for="available" class="text-sm text-gray-700">Apenas disponíveis</label>
      </div>
    </div>

    <!-- Instruments Grid -->
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="instrument in filteredInstruments" :key="instrument.id" class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
        <div class="relative">
          <img :src="instrument.image" :alt="instrument.name" class="w-full h-48 object-cover">
          <div class="absolute top-3 right-3">
            <span :class="instrument.available ? 'bg-green-500' : 'bg-red-500'" class="px-2 py-1 text-white text-xs rounded-full font-medium">
              {{ instrument.available ? 'Disponível' : 'Indisponível' }}
            </span>
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
              <User class="h-4 w-4" />
              <span>{{ instrument.provider }}</span>
            </div>
            <div class="flex items-center gap-2 text-sm text-gray-600">
              <Clock class="h-4 w-4" />
              <span>{{ instrument.availableHours }}</span>
            </div>
          </div>
          
          <button 
            @click="requestScheduling(instrument)" 
            :disabled="!instrument.available || !isLoggedIn"
            :class="[
              'w-full px-4 py-2 rounded-lg transition-colors font-medium',
              instrument.available && isLoggedIn 
                ? 'bg-blue-600 text-white hover:bg-blue-700' 
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            ]"
          >
            {{ !isLoggedIn ? 'Faça login para agendar' : instrument.available ? 'Solicitar Agendamento' : 'Indisponível' }}
          </button>
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
import { ref, computed } from 'vue'
import { MapPin, User, Clock } from 'lucide-vue-next'
import SchedulingModal from '@/components/modals/SchedulingModal.vue'

const selectedType = ref('')
const selectedBrand = ref('')
const selectedLocation = ref('')
const showAvailableOnly = ref(false)
const selectedInstrument = ref(null)
const isLoggedIn = ref(true)

const instruments = ref([
  {
    id: 1,
    name: 'Violão Clássico Yamaha C40',
    type: 'Cordas',
    brand: 'Yamaha',
    color: '#8B4513',
    colorName: 'Natural',
    description: 'Violão clássico com tampo em abeto sólido, ideal para iniciantes e estudantes. Possui excelente projeção sonora e acabamento impecável. Cordas de nylon proporcionam toque suave e confortável.',
    location: 'Centro',
    provider: 'ONG Música para Todos',
    available: true,
    availableHours: 'Seg-Sex: 14h-18h',
    image: '/placeholder.svg?height=200&width=300'
  },
  {
    id: 2,
    name: 'Teclado Yamaha PSR-E373',
    type: 'Teclas',
    brand: 'Yamaha',
    color: '#000000',
    colorName: 'Preto',
    description: 'Teclado eletrônico com 61 teclas sensíveis ao toque, 622 vozes de alta qualidade e 205 estilos de acompanhamento. Inclui função de aprendizado e conectividade USB. Perfeito para iniciantes e intermediários.',
    location: 'Zona Norte',
    provider: 'Prof. Carlos Mendes',
    available: true,
    availableHours: 'Sáb-Dom: 9h-17h',
    image: '/placeholder.svg?height=200&width=300'
  },
  {
    id: 3,
    name: 'Flauta Transversal Pearl PF-505E',
    type: 'Sopro',
    brand: 'Pearl',
    color: '#C0C0C0',
    colorName: 'Prata',
    description: 'Flauta transversal profissional em prata maciça com chaves abertas. Excelente resposta em todos os registros, ideal para estudos avançados e apresentações. Inclui estojo rígido e kit de limpeza.',
    location: 'Zona Sul',
    provider: 'Conservatório Municipal',
    available: false,
    availableHours: 'Ter-Qui: 10h-16h',
    image: '/placeholder.svg?height=200&width=300'
  },
  {
    id: 4,
    name: 'Guitarra Elétrica Fender Stratocaster',
    type: 'Cordas',
    brand: 'Fender',
    color: '#FF0000',
    colorName: 'Vermelho',
    description: 'Guitarra elétrica clássica com corpo em alder, braço em maple e escala em rosewood. Três captadores single-coil proporcionam o som característico da Stratocaster. Inclui amplificador de 15W.',
    location: 'Zona Oeste',
    provider: 'Escola de Rock',
    available: true,
    availableHours: 'Seg-Sex: 19h-22h',
    image: '/placeholder.svg?height=200&width=300'
  },
  {
    id: 5,
    name: 'Bateria Acústica Pearl Export',
    type: 'Percussão',
    brand: 'Pearl',
    color: '#000080',
    colorName: 'Azul',
    description: 'Kit completo de bateria acústica com 5 tambores, caixa, bumbo, dois tons e floor tom. Inclui pratos crash, ride e hi-hat, além de banco e baquetas. Ideal para rock, pop e jazz.',
    location: 'Centro',
    provider: 'Estúdio Ritmo & Compasso',
    available: true,
    availableHours: 'Ter-Dom: 10h-20h',
    image: '/placeholder.svg?height=200&width=300'
  },
  {
    id: 6,
    name: 'Piano Digital Casio CDP-S110',
    type: 'Teclas',
    brand: 'Casio',
    color: '#000000',
    colorName: 'Preto',
    description: 'Piano digital compacto com 88 teclas pesadas e 10 timbres de alta qualidade. Sistema de som estéreo e conectividade Bluetooth. Design elegante e portátil, perfeito para prática doméstica.',
    location: 'Zona Leste',
    provider: 'Academia Musical Harmonia',
    available: true,
    availableHours: 'Seg-Sex: 8h-18h',
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

  if (selectedBrand.value) {
    filtered = filtered.filter(instrument =>
      instrument.brand.toLowerCase().includes(selectedBrand.value.toLowerCase())
    )
  }

  if (selectedLocation.value) {
    filtered = filtered.filter(instrument =>
      instrument.location.toLowerCase().includes(selectedLocation.value.toLowerCase())
    )
  }

  if (showAvailableOnly.value) {
    filtered = filtered.filter(instrument => instrument.available)
  }

  return filtered
})

const requestScheduling = (instrument) => {
  console.log('Abrindo modal para:', instrument)
  selectedInstrument.value = instrument
}

const handleScheduled = (schedulingData) => {
  console.log('Agendamento solicitado:', schedulingData)
  selectedInstrument.value = null
}
</script>