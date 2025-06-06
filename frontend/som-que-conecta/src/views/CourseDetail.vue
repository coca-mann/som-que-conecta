<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div v-if="course" class="bg-white rounded-lg shadow-lg overflow-hidden">
      <!-- Course Header -->
      <div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-8">
        <div class="flex items-start justify-between">
          <div>
            <h1 class="text-3xl font-bold mb-2">{{ course.title }}</h1>
            <p class="text-blue-100 mb-4">{{ course.description }}</p>
            <div class="flex items-center gap-4 text-sm">
              <span class="flex items-center gap-1">
                <Clock class="h-4 w-4" />
                {{ course.duration }}
              </span>
              <span class="flex items-center gap-1">
                <BookOpen class="h-4 w-4" />
                {{ course.lessons }} aulas
              </span>
              <span class="flex items-center gap-1">
                <User class="h-4 w-4" />
                {{ course.instructor }}
              </span>
              <span class="flex items-center gap-1 bg-green-500 px-2 py-1 rounded-full text-xs font-medium">
                Gratuito
              </span>
            </div>
          </div>
          <button @click="$router.go(-1)" class="text-white hover:text-blue-200 transition-colors">
            <X class="h-6 w-6" />
          </button>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="p-6 border-b">
        <div class="flex justify-between items-center mb-2">
          <h3 class="text-lg font-semibold">Seu Progresso</h3>
          <span class="text-2xl font-bold text-blue-600">{{ progressPercentage }}%</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-3">
          <div class="bg-blue-600 h-3 rounded-full transition-all duration-500" :style="{ width: progressPercentage + '%' }"></div>
        </div>
        <p class="text-sm text-gray-600 mt-2">{{ completedTasks }} de {{ course.tasks.length }} tarefas concluídas</p>
      </div>

      <!-- Tasks List -->
      <div class="p-6">
        <h3 class="text-xl font-semibold mb-6">Tarefas do Curso</h3>
        <div class="space-y-4">
          <div v-for="(task, index) in course.tasks" :key="task.id" class="border rounded-lg p-4 hover:shadow-md transition-shadow">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-4">
                <div class="flex-shrink-0">
                  <div :class="[
                    'w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold',
                    task.completed ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
                  ]">
                    {{ index + 1 }}
                  </div>
                </div>
                <div>
                  <h4 :class="[
                    'font-medium',
                    task.completed ? 'text-green-800' : 'text-gray-900'
                  ]">
                    {{ task.title }}
                  </h4>
                  <p v-if="task.description" class="text-sm text-gray-600 mt-1">{{ task.description }}</p>
                </div>
              </div>
              
              <div class="flex items-center gap-2">
                <button 
                  v-if="task.completed"
                  class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium"
                  disabled
                >
                  <Check class="h-4 w-4 inline mr-1" />
                  Concluída
                </button>
                <button 
                  @click="goToTask(task)"
                  class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
                >
                  {{ task.completed ? 'Revisar' : 'Iniciar' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Course Actions -->
      <div class="p-6 bg-gray-50 border-t">
        <div class="flex justify-between items-center">
          <div>
            <p class="text-sm text-gray-600">
              Continue seu aprendizado e complete todas as tarefas para finalizar o curso
            </p>
          </div>
          <div class="flex gap-3">
            <button 
              v-if="progressPercentage === 100"
              class="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <Award class="h-4 w-4 inline mr-2" />
              Curso Concluído!
            </button>
            <button 
              v-else
              @click="continueFromLastTask"
              class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Continuar Estudando
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Task Completion Modal -->
    <div v-if="showCompletionModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <div class="text-center">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Check class="h-8 w-8 text-green-600" />
          </div>
          <h3 class="text-lg font-semibold mb-2">Tarefa Concluída!</h3>
          <p class="text-gray-600 mb-4">Parabéns! Você completou mais uma etapa do seu aprendizado.</p>
          <button 
            @click="showCompletionModal = false"
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Continuar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Clock, BookOpen, User, X, Check, Award } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const course = ref(null)
const showCompletionModal = ref(false)

// Mock course data - in real app, fetch from API
const courses = {
  1: {
    id: 1,
    title: 'Violão para Iniciantes',
    description: 'Aprenda os fundamentos do violão desde o básico até tocar suas primeiras músicas.',
    duration: '4 semanas',
    lessons: 12,
    instructor: 'Maria Silva',
    tasks: [
      { 
        id: 1, 
        title: 'Postura e posicionamento', 
        description: 'Aprenda a postura correta para tocar violão',
        completed: true 
      },
      { 
        id: 2, 
        title: 'Primeiros acordes', 
        description: 'Domine os acordes básicos: Am, C, D, G',
        completed: true 
      },
      { 
        id: 3, 
        title: 'Mudança entre acordes', 
        description: 'Pratique a transição suave entre acordes',
        completed: true 
      },
      { 
        id: 4, 
        title: 'Ritmo básico', 
        description: 'Aprenda padrões rítmicos fundamentais',
        completed: false 
      },
      { 
        id: 5, 
        title: 'Primeira música completa', 
        description: 'Toque sua primeira música do início ao fim',
        completed: false 
      }
    ]
  },
  2: {
    id: 2,
    title: 'Piano Clássico Básico',
    description: 'Introdução ao piano clássico com técnicas fundamentais e peças simples.',
    duration: '6 semanas',
    lessons: 18,
    instructor: 'João Santos',
    tasks: [
      { 
        id: 1, 
        title: 'Posição das mãos', 
        description: 'Aprenda a posicionar corretamente as mãos no teclado',
        completed: false 
      },
      { 
        id: 2, 
        title: 'Escalas básicas', 
        description: 'Pratique as escalas fundamentais para desenvolver técnica',
        completed: false 
      }
    ]
  }
}

const completedTasks = computed(() => {
  return course.value?.tasks.filter(task => task.completed).length || 0
})

const progressPercentage = computed(() => {
  if (!course.value?.tasks.length) return 0
  return Math.round((completedTasks.value / course.value.tasks.length) * 100)
})

const goToTask = (task) => {
  router.push(`/course/${course.value.id}/task/${task.id}`)
}

const continueFromLastTask = () => {
  // Find the first incomplete task
  const nextTask = course.value.tasks.find(task => !task.completed)
  
  if (nextTask) {
    goToTask(nextTask)
  } else {
    // If all tasks are completed, go to the first task
    goToTask(course.value.tasks[0])
  }
}

onMounted(() => {
  const courseId = parseInt(route.params.id)
  course.value = courses[courseId]
})
</script>