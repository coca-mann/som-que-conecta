<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Minicursos</h1>
      <p class="text-gray-600">Aprenda música passo a passo com nossos cursos estruturados gratuitos</p>
    </div>

    <!-- Filters -->
    <div class="mb-8 flex flex-wrap gap-4">
      <select v-model="selectedLevel" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option value="">Todos os Níveis</option>
        <option value="iniciante">Iniciante</option>
        <option value="intermediario">Intermediário</option>
        <option value="avancado">Avançado</option>
      </select>
      
      <select v-model="selectedInstrument" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option value="">Todos os Instrumentos</option>
        <option value="violao">Violão</option>
        <option value="piano">Piano</option>
        <option value="bateria">Bateria</option>
        <option value="flauta">Flauta</option>
      </select>
    </div>

    <!-- Courses Grid -->
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="course in filteredCourses" :key="course.id" class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
        <img :src="course.image" :alt="course.title" class="w-full h-48 object-cover">
        
        <div class="p-6">
          <div class="flex items-center gap-2 mb-2">
            <span class="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">{{ course.level }}</span>
            <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">{{ course.instrument }}</span>
            <span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">Gratuito</span>
          </div>
          
          <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ course.title }}</h3>
          <p class="text-gray-600 mb-4">{{ course.description }}</p>
          
          <div class="space-y-2 mb-4">
            <div class="flex items-center justify-between text-sm text-gray-600">
              <div class="flex items-center gap-2">
                <Clock class="h-4 w-4" />
                <span>{{ course.duration }}</span>
              </div>
              <div class="flex items-center gap-2">
                <BookOpen class="h-4 w-4" />
                <span>{{ course.lessons }} aulas</span>
              </div>
            </div>
            
            <div v-if="isLoggedIn && course.progress !== undefined" class="space-y-1">
              <div class="flex justify-between text-sm">
                <span>Progresso</span>
                <span>{{ course.progress }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-blue-600 h-2 rounded-full transition-all duration-300" :style="{ width: course.progress + '%' }"></div>
              </div>
            </div>
          </div>
          
          <button 
            @click="accessCourse(course)" 
            :class="[
              'w-full px-4 py-2 rounded-lg transition-colors',
              isLoggedIn 
                ? 'bg-blue-600 text-white hover:bg-blue-700' 
                : 'bg-gray-600 text-white hover:bg-gray-700'
            ]"
          >
            {{ isLoggedIn ? (course.progress > 0 ? 'Continuar Curso' : 'Iniciar Curso') : 'Ver Descrição' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Clock, BookOpen } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()
const selectedLevel = ref('')
const selectedInstrument = ref('')
const isLoggedIn = ref(false) // Should come from auth store

const courses = ref([
  {
    id: 1,
    title: 'Violão para Iniciantes',
    description: 'Aprenda os fundamentos do violão desde o básico até tocar suas primeiras músicas.',
    level: 'Iniciante',
    instrument: 'Violão',
    duration: '4 semanas',
    lessons: 12,
    progress: 25,
    image: '/placeholder.svg?height=200&width=300',
    instructor: 'Maria Silva',
    tasks: [
      { id: 1, title: 'Postura e posicionamento', completed: true },
      { id: 2, title: 'Primeiros acordes', completed: true },
      { id: 3, title: 'Mudança entre acordes', completed: true },
      { id: 4, title: 'Ritmo básico', completed: false }
    ]
  },
  {
    id: 2,
    title: 'Piano Clássico Básico',
    description: 'Introdução ao piano clássico com técnicas fundamentais e peças simples.',
    level: 'Iniciante',
    instrument: 'Piano',
    duration: '6 semanas',
    lessons: 18,
    progress: 0,
    image: '/placeholder.svg?height=200&width=300',
    instructor: 'João Santos',
    tasks: [
      { id: 1, title: 'Posição das mãos', completed: false },
      { id: 2, title: 'Escalas básicas', completed: false },
      { id: 3, title: 'Leitura de partitura', completed: false }
    ]
  }
])

const filteredCourses = computed(() => {
  let filtered = courses.value

  if (selectedLevel.value) {
    filtered = filtered.filter(course => 
      course.level.toLowerCase().includes(selectedLevel.value.toLowerCase())
    )
  }

  if (selectedInstrument.value) {
    filtered = filtered.filter(course =>
      course.instrument.toLowerCase().includes(selectedInstrument.value.toLowerCase())
    )
  }

  return filtered
})

const accessCourse = (course) => {
  router.push(`/course/${course.id}`)
}
</script>