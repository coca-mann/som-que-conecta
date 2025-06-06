<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Course Navigation Header -->
      <div class="bg-white rounded-lg shadow-md p-4 mb-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <button @click="goBackToCourse" class="p-2 text-gray-600 hover:text-blue-600 transition-colors">
              <ArrowLeft class="h-5 w-5" />
            </button>
            <div>
              <h1 class="text-xl font-bold text-gray-900">{{ course?.title }}</h1>
              <div class="flex items-center gap-2 text-sm text-gray-600">
                <span>Tarefa {{ currentTaskIndex + 1 }} de {{ course?.tasks.length }}</span>
                <span>•</span>
                <span>{{ task?.title }}</span>
              </div>
            </div>
          </div>
          
          <div class="hidden md:block">
            <div class="flex items-center gap-2">
              <div class="text-sm text-gray-600">Progresso do curso:</div>
              <div class="w-48 bg-gray-200 rounded-full h-2">
                <div class="bg-blue-600 h-2 rounded-full transition-all duration-300" :style="{ width: `${courseProgress}%` }"></div>
              </div>
              <div class="text-sm font-medium text-blue-600">{{ courseProgress }}%</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Task Content -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden mb-6">
        <!-- Video Section -->
        <div class="relative w-full" style="padding-top: 56.25%;">
          <div class="absolute top-0 left-0 w-full h-full bg-black">
            <div v-if="task?.videoUrl" class="w-full h-full">
              <iframe 
                :src="task.videoUrl" 
                class="w-full h-full" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen
              ></iframe>
            </div>
            <div v-else class="w-full h-full flex items-center justify-center text-white">
              <Play class="h-16 w-16 mx-auto mb-4 opacity-50" />
              <p>Vídeo não disponível</p>
            </div>
          </div>
        </div>

        <!-- Task Details -->
        <div class="p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">{{ task?.title }}</h2>
          
          <div class="prose max-w-none mb-8">
            <p>{{ task?.description }}</p>
            
            <div v-if="task?.content" v-html="task.content" class="mt-4"></div>
          </div>
          
          <!-- Task Resources -->
          <div v-if="task?.resources && task.resources.length > 0" class="mb-8">
            <h3 class="text-lg font-semibold text-gray-900 mb-3">Recursos Adicionais</h3>
            <div class="space-y-2">
              <a 
                v-for="resource in task.resources" 
                :key="resource.id" 
                :href="resource.url" 
                target="_blank" 
                class="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div class="p-2 bg-blue-100 text-blue-600 rounded-lg">
                  <FileText v-if="resource.type === 'pdf'" class="h-5 w-5" />
                  <Music v-else-if="resource.type === 'audio'" class="h-5 w-5" />
                  <Link v-else class="h-5 w-5" />
                </div>
                <div>
                  <div class="font-medium text-gray-900">{{ resource.title }}</div>
                  <div class="text-sm text-gray-600">{{ resource.description }}</div>
                </div>
              </a>
            </div>
          </div>
          
          <!-- Task Completion -->
          <div class="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-gray-200">
            <div class="flex items-center gap-2">
              <div v-if="task?.completed" class="flex items-center gap-2 text-green-600">
                <CheckCircle class="h-5 w-5" />
                <span class="font-medium">Tarefa concluída</span>
              </div>
              <div v-else class="text-gray-600">
                <span>Marque como concluída quando terminar esta tarefa</span>
              </div>
            </div>
            
            <button 
              @click="toggleTaskCompletion" 
              :class="[
                'px-6 py-2 rounded-lg font-medium transition-colors',
                task?.completed 
                  ? 'bg-gray-100 text-gray-600 hover:bg-gray-200' 
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              ]"
            >
              {{ task?.completed ? 'Marcar como não concluída' : 'Marcar como concluída' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="flex justify-between">
        <button 
          @click="navigateToPreviousTask" 
          :disabled="currentTaskIndex === 0"
          :class="[
            'flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-colors',
            currentTaskIndex === 0
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-white text-gray-700 hover:bg-gray-100'
          ]"
        >
          <ChevronLeft class="h-5 w-5" />
          Tarefa Anterior
        </button>
        
        <button 
          @click="navigateToNextTask" 
          :disabled="currentTaskIndex === course?.tasks.length - 1"
          :class="[
            'flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-colors',
            currentTaskIndex === course?.tasks.length - 1
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          ]"
        >
          Próxima Tarefa
          <ChevronRight class="h-5 w-5" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  ArrowLeft, 
  Play, 
  CheckCircle, 
  ChevronLeft, 
  ChevronRight,
  FileText,
  Music,
  Link
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const course = ref(null)
const task = ref(null)
const currentTaskIndex = ref(0)

// Mock courses data - in real app, fetch from API
const coursesData = {
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
        description: 'Aprenda a postura correta para tocar violão e como posicionar as mãos no instrumento.',
        content: `
          <h3>Postura Correta</h3>
          <p>Uma postura adequada é fundamental para tocar violão confortavelmente e evitar lesões. Siga estas orientações:</p>
          <ul>
            <li>Sente-se na borda da cadeira com as costas retas</li>
            <li>Apoie o violão na perna direita (para destros) ou esquerda (para canhotos)</li>
            <li>Mantenha o braço do violão ligeiramente inclinado para cima</li>
            <li>Relaxe os ombros e mantenha os cotovelos afastados do corpo</li>
          </ul>
          
          <h3>Posicionamento das Mãos</h3>
          <p>O posicionamento correto das mãos é essencial para tocar com precisão:</p>
          <ul>
            <li>Mão do braço: Mantenha o polegar na parte de trás do braço, aproximadamente no meio</li>
            <li>Dedos curvados e pressionando as cordas com as pontas</li>
            <li>Mão de palhetada: Mantenha o pulso relaxado e levemente arqueado</li>
          </ul>
        `,
        videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        completed: true,
        resources: [
          {
            id: 1,
            title: 'Guia de Postura para Violão',
            description: 'PDF com ilustrações detalhadas',
            type: 'pdf',
            url: '#'
          },
          {
            id: 2,
            title: 'Exercícios de Aquecimento',
            description: 'Áudio com exercícios para aquecer as mãos',
            type: 'audio',
            url: '#'
          }
        ]
      },
      { 
        id: 2, 
        title: 'Primeiros acordes', 
        description: 'Aprenda os acordes básicos que serão a base para tocar diversas músicas.',
        content: `
          <h3>Acordes Básicos</h3>
          <p>Vamos aprender os acordes mais importantes para iniciantes:</p>
          <ul>
            <li><strong>Acorde de Dó (C):</strong> Posicione o dedo 3 na terceira casa da quinta corda, o dedo 2 na segunda casa da quarta corda e o dedo 1 na primeira casa da segunda corda.</li>
            <li><strong>Acorde de Sol (G):</strong> Posicione o dedo 2 na terceira casa da sexta corda, o dedo 1 na segunda casa da quinta corda e o dedo 3 na terceira casa da primeira corda.</li>
            <li><strong>Acorde de Ré (D):</strong> Posicione os dedos 1, 2 e 3 na segunda casa das três primeiras cordas.</li>
          </ul>
          
          <p>Pratique a transição entre esses acordes lentamente, garantindo que todas as notas soem claramente.</p>
        `,
        videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        completed: true,
        resources: [
          {
            id: 3,
            title: 'Diagrama de Acordes',
            description: 'PDF com todos os acordes básicos',
            type: 'pdf',
            url: '#'
          }
        ]
      },
      { 
        id: 3, 
        title: 'Mudança entre acordes', 
        description: 'Aprenda a fazer transições suaves entre diferentes acordes.',
        content: `
          <h3>Técnicas de Transição</h3>
          <p>A mudança fluida entre acordes é um dos maiores desafios para iniciantes. Aqui estão algumas dicas:</p>
          <ul>
            <li>Pratique lentamente, aumentando a velocidade gradualmente</li>
            <li>Identifique "dedos âncora" que permanecem na mesma posição entre acordes</li>
            <li>Mova todos os dedos simultaneamente, não um de cada vez</li>
            <li>Pratique a sequência C - G - D - C repetidamente</li>
          </ul>
          
          <p>Dedique pelo menos 10 minutos por dia apenas para praticar transições entre acordes.</p>
        `,
        videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        completed: true,
        resources: []
      },
      { 
        id: 4, 
        title: 'Ritmo básico', 
        description: 'Aprenda padrões rítmicos fundamentais para acompanhamento.',
        content: `
          <h3>Padrões Rítmicos</h3>
          <p>O ritmo é o que dá vida às progressões de acordes. Vamos aprender o padrão básico de batida:</p>
          <ul>
            <li>Batida para baixo: ↓</li>
            <li>Batida para cima: ↑</li>
            <li>Padrão básico: ↓ ↓↑ ↓ ↑</li>
          </ul>
          
          <p>Pratique este padrão lentamente com um metrônomo, começando em 60 BPM e aumentando gradualmente.</p>
          
          <h3>Exercício Prático</h3>
          <p>Toque o acorde de Dó (C) usando o padrão rítmico acima por 4 compassos, depois mude para Sol (G) por mais 4 compassos.</p>
        `,
        videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        completed: false,
        resources: [
          {
            id: 4,
            title: 'Exercícios de Ritmo',
            description: 'Áudio com diferentes padrões rítmicos',
            type: 'audio',
            url: '#'
          },
          {
            id: 5,
            title: 'Guia de Notação Rítmica',
            description: 'Aprenda a ler padrões rítmicos',
            type: 'pdf',
            url: '#'
          }
        ]
      },
      { 
        id: 5, 
        title: 'Primeira música completa', 
        description: 'Aprenda a tocar sua primeira música do início ao fim.',
        content: `
          <h3>Sua Primeira Música</h3>
          <p>Agora vamos aplicar tudo o que aprendemos para tocar "Parabéns pra Você", uma música simples com apenas 3 acordes:</p>
          
          <p><strong>Versos:</strong></p>
          <p>C - G - C (Parabéns pra você)</p>
          <p>C - G - C (Nesta data querida)</p>
          <p>C - C7 - F - C (Muitas felicidades)</p>
          <p>G - C (Muitos anos de vida)</p>
          
          <p>Siga o vídeo para aprender o ritmo exato e como cantar junto com o acompanhamento.</p>
        `,
        videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        completed: false,
        resources: [
          {
            id: 6,
            title: 'Cifra Completa',
            description: 'PDF com a cifra da música',
            type: 'pdf',
            url: '#'
          },
          {
            id: 7,
            title: 'Playback para Prática',
            description: 'Áudio sem violão para você praticar',
            type: 'audio',
            url: '#'
          }
        ]
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
        description: 'Aprenda a posicionar corretamente as mãos no teclado.',
        videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        completed: false,
        resources: []
      },
      { 
        id: 2, 
        title: 'Escalas básicas', 
        description: 'Pratique as escalas fundamentais para desenvolver técnica.',
        videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        completed: false,
        resources: []
      }
    ]
  }
}

const courseProgress = computed(() => {
  if (!course.value || !course.value.tasks.length) return 0
  
  const completedTasks = course.value.tasks.filter(t => t.completed).length
  return Math.round((completedTasks / course.value.tasks.length) * 100)
})

const goBackToCourse = () => {
  router.push(`/course/${route.params.courseId}`)
}

const toggleTaskCompletion = () => {
  if (task.value) {
    task.value.completed = !task.value.completed
    
    // Update the task in the course object
    const taskIndex = course.value.tasks.findIndex(t => t.id === task.value.id)
    if (taskIndex !== -1) {
      course.value.tasks[taskIndex].completed = task.value.completed
    }
    
    // Here you would send an API request to update the task status
    console.log('Task completion toggled:', task.value.id, task.value.completed)
  }
}

const navigateToPreviousTask = () => {
  if (currentTaskIndex.value > 0) {
    const previousTask = course.value.tasks[currentTaskIndex.value - 1]
    router.push(`/course/${route.params.courseId}/task/${previousTask.id}`)
  }
}

const navigateToNextTask = () => {
  if (currentTaskIndex.value < course.value.tasks.length - 1) {
    const nextTask = course.value.tasks[currentTaskIndex.value + 1]
    router.push(`/course/${route.params.courseId}/task/${nextTask.id}`)
  }
}

const loadTask = () => {
  const courseId = parseInt(route.params.courseId)
  const taskId = parseInt(route.params.taskId)
  
  course.value = coursesData[courseId]
  
  if (course.value) {
    const taskIndex = course.value.tasks.findIndex(t => t.id === taskId)
    
    if (taskIndex !== -1) {
      task.value = course.value.tasks[taskIndex]
      currentTaskIndex.value = taskIndex
    } else {
      // Se a tarefa não for encontrada, redireciona para a primeira tarefa
      const firstTask = course.value.tasks[0]
      router.push(`/course/${courseId}/task/${firstTask.id}`)
    }
  } else {
    console.error('Course not found')
    router.push('/courses')
  }
}

watch(() => route.params, loadTask, { immediate: true })

onMounted(() => {
  loadTask()
})
</script>

<style scoped>
.aspect-w-16,
.aspect-h-9 {
  position: static;
  padding-bottom: 0;
}

.prose h3 {
  @apply text-xl font-semibold text-gray-900 mt-6 mb-3;
}

.prose p {
  @apply text-gray-700 leading-relaxed mb-4;
}

.prose ul {
  @apply list-disc list-inside space-y-2 mb-4 text-gray-700;
}

.prose li {
  @apply ml-4;
}

.prose strong {
  @apply font-semibold text-gray-900;
}
</style>