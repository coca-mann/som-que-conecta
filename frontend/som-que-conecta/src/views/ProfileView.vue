<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Meu Perfil</h1>
            <p class="text-gray-600">Gerencie suas informações pessoais e acompanhe seu progresso</p>
          </div>
          
          <button 
            @click="toggleEditMode" 
            :class="[
              'px-6 py-2 rounded-lg transition-colors flex items-center gap-2',
              isEditing ? 'bg-green-600 text-white hover:bg-green-700' : 'bg-blue-600 text-white hover:bg-blue-700'
            ]"
          >
            <component :is="isEditing ? Save : Edit" class="h-5 w-5" />
            {{ isEditing ? 'Salvar Alterações' : 'Editar Perfil' }}
          </button>
        </div>
      </div>

      <div class="grid lg:grid-cols-3 gap-6">
        <!-- Left Column - Profile Info -->
        <div class="lg:col-span-1 space-y-6">
          <!-- Profile Picture & Basic Info -->
          <div class="bg-white rounded-lg shadow-sm p-6">
            <div class="text-center">
              <!-- Profile Picture -->
              <div class="relative inline-block mb-4">
                <div class="w-32 h-32 rounded-full overflow-hidden bg-gray-200 mx-auto relative">
                  <img 
                    v-if="userProfile.avatar" 
                    :src="userProfile.avatar" 
                    :alt="userProfile.name"
                    class="w-full h-full object-cover"
                  >
                  <div v-else class="w-full h-full flex items-center justify-center">
                    <User class="h-16 w-16 text-gray-400" />
                  </div>
                  
                  <!-- Edit Photo Button -->
                  <button 
                    v-if="isEditing"
                    @click="$refs.avatarInput.click()"
                    class="absolute bottom-0 left-1/2 -translate-x-1/2 p-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors shadow-lg"
                  >
                    <Camera class="h-4 w-4" />
                  </button>
                </div>
                
                <input 
                  ref="avatarInput"
                  type="file" 
                  accept="image/*"
                  @change="handleAvatarUpload"
                  class="hidden"
                >
              </div>

              <!-- Name -->
              <div v-if="!isEditing">
                <h2 class="text-2xl font-bold text-gray-900">{{ userProfile.name }} {{ userProfile.lastName }}</h2>
                <p class="text-gray-600 mt-1">{{ userProfile.email }}</p>
                <div class="flex items-center justify-center gap-2 mt-2">
                  <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                    {{ userProfile.level }}
                  </span>
                  <span class="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">
                    {{ userProfile.gender === 'M' ? 'Masculino' : userProfile.gender === 'F' ? 'Feminino' : 'Outro' }}
                  </span>
                </div>
              </div>

              <!-- Edit Form -->
              <div v-else class="space-y-4">
                <div class="grid grid-cols-2 gap-3">
                  <input 
                    v-model="editForm.name" 
                    type="text" 
                    placeholder="Nome"
                    class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  >
                  <input 
                    v-model="editForm.lastName" 
                    type="text" 
                    placeholder="Sobrenome"
                    class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  >
                </div>
                
                <select 
                  v-model="editForm.gender" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                >
                  <option value="">Selecione o sexo</option>
                  <option value="M">Masculino</option>
                  <option value="F">Feminino</option>
                  <option value="O">Outro</option>
                  <option value="N">Prefiro não informar</option>
                </select>

                <input 
                  v-model="editForm.email" 
                  type="email" 
                  placeholder="Email"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                >
              </div>
            </div>

            <!-- Stats -->
            <div class="grid grid-cols-3 gap-4 mt-6 pt-6 border-t border-gray-200">
              <div class="text-center">
                <div class="text-2xl font-bold text-blue-600">{{ userStats.totalCourses }}</div>
                <div class="text-sm text-gray-600">Cursos</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-green-600">{{ userStats.totalInstruments }}</div>
                <div class="text-sm text-gray-600">Instrumentos</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-purple-600">{{ userStats.totalHours }}</div>
                <div class="text-sm text-gray-600">Horas</div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="bg-white rounded-lg shadow-sm p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Ações Rápidas</h3>
            <div class="space-y-3">
              <router-link 
                to="/manage-instruments" 
                class="flex items-center gap-3 p-3 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors"
              >
                <Music class="h-5 w-5" />
                <span>Gerenciar Instrumentos</span>
                <ChevronRight class="h-4 w-4 ml-auto" />
              </router-link>
              
              <router-link 
                to="/courses" 
                class="flex items-center gap-3 p-3 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors"
              >
                <BookOpen class="h-5 w-5" />
                <span>Ver Todos os Cursos</span>
                <ChevronRight class="h-4 w-4 ml-auto" />
              </router-link>
              
              <router-link 
                to="/articles/create" 
                class="flex items-center gap-3 p-3 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors"
              >
                <PenTool class="h-5 w-5" />
                <span>Criar Artigo</span>
                <ChevronRight class="h-4 w-4 ml-auto" />
              </router-link>
            </div>
          </div>
        </div>

        <!-- Right Column - Dashboard -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Current Courses -->
          <div class="bg-white rounded-lg shadow-sm p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-xl font-semibold text-gray-900">Cursos em Andamento</h3>
              <router-link 
                to="/courses" 
                class="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center gap-1"
              >
                Ver todos
                <ChevronRight class="h-4 w-4" />
              </router-link>
            </div>

            <div class="grid md:grid-cols-2 gap-4">
              <div v-for="course in currentCourses" :key="course.id" class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div class="flex items-start gap-4">
                  <img :src="course.image" :alt="course.title" class="w-16 h-16 rounded-lg object-cover">
                  <div class="flex-1 min-w-0">
                    <h4 class="font-semibold text-gray-900 truncate">{{ course.title }}</h4>
                    <p class="text-sm text-gray-600 mb-2">{{ course.instructor }}</p>
                    
                    <!-- Progress Bar -->
                    <div class="space-y-1">
                      <div class="flex justify-between text-sm">
                        <span class="text-gray-600">Progresso</span>
                        <span class="font-medium">{{ course.progress }}%</span>
                      </div>
                      <div class="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          class="bg-blue-600 h-2 rounded-full transition-all duration-300" 
                          :style="{ width: course.progress + '%' }"
                        ></div>
                      </div>
                    </div>
                    
                    <div class="flex items-center justify-between mt-3">
                      <span class="text-xs text-gray-500">{{ course.completedLessons }}/{{ course.totalLessons }} aulas</span>
                      <button 
                        @click="continueCourse(course)"
                        class="px-3 py-1 bg-blue-600 text-white text-xs rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        Continuar
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="currentCourses.length === 0" class="text-center py-8">
              <BookOpen class="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h4 class="text-lg font-medium text-gray-900 mb-2">Nenhum curso em andamento</h4>
              <p class="text-gray-600 mb-4">Comece sua jornada musical hoje mesmo!</p>
              <router-link 
                to="/courses" 
                class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Explorar Cursos
              </router-link>
            </div>
          </div>

          <!-- My Instruments -->
          <div class="bg-white rounded-lg shadow-sm p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-xl font-semibold text-gray-900">Meus Instrumentos</h3>
              <router-link 
                to="/manage-instruments" 
                class="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center gap-1"
              >
                Gerenciar
                <ChevronRight class="h-4 w-4" />
              </router-link>
            </div>

            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="instrument in userInstruments" :key="instrument.id" class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div class="text-center">
                  <img :src="instrument.image" :alt="instrument.name" class="w-20 h-20 rounded-lg object-cover mx-auto mb-3">
                  <h4 class="font-semibold text-gray-900 mb-1">{{ instrument.name }}</h4>
                  <p class="text-sm text-gray-600 mb-2">{{ instrument.brand }}</p>
                  
                  <div class="flex items-center justify-center gap-2 mb-3">
                    <span :class="[
                      'px-2 py-1 text-xs rounded-full',
                      instrument.condition === 'excellent' ? 'bg-green-100 text-green-800' :
                      instrument.condition === 'good' ? 'bg-blue-100 text-blue-800' :
                      instrument.condition === 'fair' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    ]">
                      {{ getConditionLabel(instrument.condition) }}
                    </span>
                  </div>
                  
                  <div class="text-xs text-gray-500">
                    Adquirido em {{ formatDate(instrument.acquiredDate) }}
                  </div>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="userInstruments.length === 0" class="text-center py-8">
              <Music class="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h4 class="text-lg font-medium text-gray-900 mb-2">Nenhum instrumento cadastrado</h4>
              <p class="text-gray-600 mb-4">Adicione seus instrumentos para melhor organização</p>
              <router-link 
                to="/manage-instruments" 
                class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                Adicionar Instrumento
              </router-link>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="bg-white rounded-lg shadow-sm p-6">
            <h3 class="text-xl font-semibold text-gray-900 mb-6">Atividade Recente</h3>
            
            <div class="space-y-4">
              <div v-for="activity in recentActivity" :key="activity.id" class="flex items-start gap-4 p-3 bg-gray-50 rounded-lg">
                <div :class="[
                  'p-2 rounded-full',
                  activity.type === 'course' ? 'bg-blue-100 text-blue-600' :
                  activity.type === 'instrument' ? 'bg-green-100 text-green-600' :
                  'bg-purple-100 text-purple-600'
                ]">
                  <component :is="getActivityIcon(activity.type)" class="h-4 w-4" />
                </div>
                
                <div class="flex-1">
                  <p class="text-sm text-gray-900">{{ activity.description }}</p>
                  <p class="text-xs text-gray-500 mt-1">{{ formatRelativeTime(activity.date) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Learning Goals -->
          <div class="bg-white rounded-lg shadow-sm p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-xl font-semibold text-gray-900">Metas de Aprendizado</h3>
              <button 
                @click="showGoalsModal = true"
                class="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center gap-1"
              >
                <Plus class="h-4 w-4" />
                Nova Meta
              </button>
            </div>

            <div class="space-y-4">
              <div v-for="goal in learningGoals" :key="goal.id" class="border border-gray-200 rounded-lg p-4">
                <div class="flex items-start justify-between mb-3">
                  <div>
                    <h4 class="font-semibold text-gray-900">{{ goal.title }}</h4>
                    <p class="text-sm text-gray-600">{{ goal.description }}</p>
                  </div>
                  <span :class="[
                    'px-2 py-1 text-xs rounded-full',
                    goal.status === 'completed' ? 'bg-green-100 text-green-800' :
                    goal.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  ]">
                    {{ getGoalStatusLabel(goal.status) }}
                  </span>
                </div>
                
                <div class="space-y-1">
                  <div class="flex justify-between text-sm">
                    <span class="text-gray-600">Progresso</span>
                    <span class="font-medium">{{ goal.progress }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      :class="[
                        'h-2 rounded-full transition-all duration-300',
                        goal.status === 'completed' ? 'bg-green-600' : 'bg-blue-600'
                      ]"
                      :style="{ width: goal.progress + '%' }"
                    ></div>
                  </div>
                </div>
                
                <div class="flex items-center justify-between mt-3 text-xs text-gray-500">
                  <span>Prazo: {{ formatDate(goal.deadline) }}</span>
                  <span>{{ goal.daysLeft }} dias restantes</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Goals Modal -->
    <div v-if="showGoalsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg w-full max-w-md mx-4">
        <div class="p-6 border-b border-gray-200 flex justify-between items-center">
          <h3 class="text-lg font-semibold">Nova Meta de Aprendizado</h3>
          <button @click="showGoalsModal = false" class="text-gray-400 hover:text-gray-600">
            <X class="h-6 w-6" />
          </button>
        </div>
        <div class="p-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Título da Meta</label>
              <input 
                v-model="newGoal.title"
                type="text" 
                placeholder="Ex: Aprender 5 acordes básicos"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Descrição</label>
              <textarea 
                v-model="newGoal.description"
                rows="3"
                placeholder="Descreva sua meta em detalhes..."
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              ></textarea>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Prazo</label>
              <input 
                v-model="newGoal.deadline"
                type="date" 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
            </div>
          </div>
          
          <div class="flex gap-3 mt-6">
            <button 
              @click="showGoalsModal = false"
              class="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Cancelar
            </button>
            <button 
              @click="addGoal"
              class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Criar Meta
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  User, 
  Edit, 
  Save, 
  Camera, 
  Music, 
  BookOpen, 
  PenTool, 
  ChevronRight, 
  Plus,
  X,
  Target,
  Clock,
  Award
} from 'lucide-vue-next'

const router = useRouter()
const isEditing = ref(false)
const showGoalsModal = ref(false)
const avatarInput = ref(null)

const userProfile = ref({
  id: 1,
  name: 'João',
  lastName: 'Silva',
  email: 'joao.silva@email.com',
  avatar: '/placeholder.svg?height=128&width=128',
  gender: 'M',
  level: 'Intermediário',
  joinDate: new Date('2023-06-15'),
  bio: 'Apaixonado por música há mais de 10 anos. Toco violão e piano.'
})

const editForm = ref({
  name: userProfile.value.name,
  lastName: userProfile.value.lastName,
  email: userProfile.value.email,
  gender: userProfile.value.gender,
  avatar: userProfile.value.avatar
})

const userStats = ref({
  totalCourses: 8,
  totalInstruments: 3,
  totalHours: 127,
  completedCourses: 3,
  articlesWritten: 2
})

const currentCourses = ref([
  {
    id: 1,
    title: 'Violão para Iniciantes',
    instructor: 'Carlos Mendes',
    image: '/placeholder.svg?height=64&width=64',
    progress: 75,
    completedLessons: 15,
    totalLessons: 20,
    lastAccessed: new Date('2024-01-20')
  },
  {
    id: 2,
    title: 'Teoria Musical Avançada',
    instructor: 'Ana Carolina',
    image: '/placeholder.svg?height=64&width=64',
    progress: 45,
    completedLessons: 9,
    totalLessons: 20,
    lastAccessed: new Date('2024-01-18')
  },
  {
    id: 3,
    title: 'Piano Clássico',
    instructor: 'Maria Fernanda',
    image: '/placeholder.svg?height=64&width=64',
    progress: 30,
    completedLessons: 6,
    totalLessons: 20,
    lastAccessed: new Date('2024-01-15')
  }
])

const userInstruments = ref([
  {
    id: 1,
    name: 'Violão Yamaha',
    brand: 'Yamaha',
    type: 'Violão',
    color: 'Natural',
    condition: 'excellent',
    image: '/placeholder.svg?height=80&width=80',
    acquiredDate: new Date('2023-03-15'),
    description: 'Violão clássico em excelente estado'
  },
  {
    id: 2,
    name: 'Piano Digital',
    brand: 'Casio',
    type: 'Piano',
    color: 'Preto',
    condition: 'good',
    image: '/placeholder.svg?height=80&width=80',
    acquiredDate: new Date('2023-08-20'),
    description: 'Piano digital com 88 teclas'
  },
  {
    id: 3,
    name: 'Ukulele Soprano',
    brand: 'Kala',
    type: 'Ukulele',
    color: 'Mahogany',
    condition: 'excellent',
    image: '/placeholder.svg?height=80&width=80',
    acquiredDate: new Date('2024-01-10'),
    description: 'Ukulele soprano tradicional'
  }
])

const recentActivity = ref([
  {
    id: 1,
    type: 'course',
    description: 'Completou a aula "Acordes Básicos" do curso Violão para Iniciantes',
    date: new Date('2024-01-20T14:30:00')
  },
  {
    id: 2,
    type: 'instrument',
    description: 'Adicionou novo instrumento: Ukulele Soprano',
    date: new Date('2024-01-18T10:15:00')
  },
  {
    id: 3,
    type: 'article',
    description: 'Publicou o artigo "Dicas para Iniciantes no Violão"',
    date: new Date('2024-01-15T16:45:00')
  },
  {
    id: 4,
    type: 'course',
    description: 'Iniciou o curso "Piano Clássico"',
    date: new Date('2024-01-12T09:20:00')
  }
])

const learningGoals = ref([
  {
    id: 1,
    title: 'Dominar 10 acordes básicos',
    description: 'Aprender e praticar os 10 acordes mais utilizados no violão',
    progress: 80,
    status: 'in_progress',
    deadline: new Date('2024-02-15'),
    daysLeft: 25
  },
  {
    id: 2,
    title: 'Tocar primeira música completa',
    description: 'Conseguir tocar uma música completa no piano',
    progress: 100,
    status: 'completed',
    deadline: new Date('2024-01-30'),
    daysLeft: 0
  },
  {
    id: 3,
    title: 'Estudar teoria musical',
    description: 'Completar curso básico de teoria musical',
    progress: 45,
    status: 'in_progress',
    deadline: new Date('2024-03-01'),
    daysLeft: 40
  }
])

const newGoal = ref({
  title: '',
  description: '',
  deadline: ''
})

const toggleEditMode = () => {
  if (isEditing.value) {
    // Save changes
    Object.assign(userProfile.value, editForm.value)
    console.log('Profile updated:', userProfile.value)
  } else {
    // Enter edit mode
    Object.assign(editForm.value, userProfile.value)
  }
  isEditing.value = !isEditing.value
}

const handleAvatarUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    alert('Por favor, selecione apenas arquivos de imagem.')
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    alert('O arquivo deve ter no máximo 5MB.')
    return
  }

  const reader = new FileReader()
  reader.onload = (e) => {
    editForm.value.avatar = e.target.result
  }
  reader.readAsDataURL(file)
}

const continueCourse = (course) => {
  // Encontra a primeira tarefa não concluída ou a última tarefa concluída
  const nextTaskIndex = course.completedLessons
  const taskId = course.totalLessons > nextTaskIndex ? nextTaskIndex + 1 : nextTaskIndex
  router.push(`/course/${course.id}/task/${taskId}`)
}

const getConditionLabel = (condition) => {
  const labels = {
    excellent: 'Excelente',
    good: 'Bom',
    fair: 'Regular',
    poor: 'Ruim'
  }
  return labels[condition] || condition
}

const getActivityIcon = (type) => {
  const icons = {
    course: BookOpen,
    instrument: Music,
    article: PenTool
  }
  return icons[type] || BookOpen
}

const getGoalStatusLabel = (status) => {
  const labels = {
    completed: 'Concluída',
    in_progress: 'Em Andamento',
    pending: 'Pendente'
  }
  return labels[status] || status
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('pt-BR', { 
    day: 'numeric', 
    month: 'short',
    year: 'numeric' 
  }).format(date)
}

const formatRelativeTime = (date) => {
  const now = new Date()
  const diffInHours = Math.floor((now - date) / (1000 * 60 * 60))
  
  if (diffInHours < 1) return 'Agora mesmo'
  if (diffInHours < 24) return `${diffInHours}h atrás`
  
  const diffInDays = Math.floor(diffInHours / 24)
  if (diffInDays < 7) return `${diffInDays}d atrás`
  
  return formatDate(date)
}

const addGoal = () => {
  if (!newGoal.value.title || !newGoal.value.deadline) {
    alert('Por favor, preencha pelo menos o título e o prazo.')
    return
  }

  const deadline = new Date(newGoal.value.deadline)
  const now = new Date()
  const daysLeft = Math.ceil((deadline - now) / (1000 * 60 * 60 * 24))

  learningGoals.value.push({
    id: Date.now(),
    title: newGoal.value.title,
    description: newGoal.value.description,
    progress: 0,
    status: 'pending',
    deadline: deadline,
    daysLeft: Math.max(0, daysLeft)
  })

  // Reset form
  newGoal.value = {
    title: '',
    description: '',
    deadline: ''
  }
  
  showGoalsModal.value = false
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>