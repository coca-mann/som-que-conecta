<template>
  <div class="min-h-screen bg-gray-50">
    <div
      v-if="isLoading"
      class="flex items-center justify-center min-h-screen"
    >
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto" />
        <p class="mt-4 text-gray-600">
          Carregando...
        </p>
      </div>
    </div>

    <div
      v-else-if="error"
      class="flex items-center justify-center min-h-screen"
    >
      <div class="text-center text-red-600">
        <p>{{ error }}</p>
        <button
          class="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          @click="fetchCourseData"
        >
          Tentar novamente
        </button>
      </div>
    </div>

    <div
      v-else-if="course && task"
      class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8"
    >
      <!-- Course Navigation Header -->
      <div class="bg-white rounded-lg shadow-md p-4 mb-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <button
              class="p-2 text-gray-600 hover:text-blue-600 transition-colors"
              @click="goBackToCourse"
            >
              <ArrowLeft class="h-5 w-5" />
            </button>
            <div>
              <h1 class="text-xl font-bold text-gray-900">
                {{ course?.title }}
              </h1>
              <div class="flex items-center gap-2 text-sm text-gray-600">
                <span>Tarefa {{ currentTaskIndex + 1 }} de {{ course?.tasks.length }}</span>
                <span>•</span>
                <span>{{ task?.title }}</span>
              </div>
            </div>
          </div>
          
          <div class="hidden md:block">
            <div class="flex items-center gap-2">
              <div class="text-sm text-gray-600">
                Progresso do curso:
              </div>
              <div class="w-48 bg-gray-200 rounded-full h-2">
                <div
                  class="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  :style="{ width: `${courseProgress}%` }"
                />
              </div>
              <div class="text-sm font-medium text-blue-600">
                {{ courseProgress }}%
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Task Content -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden mb-6">
        <!-- Video Section -->
        <div
          class="relative w-full"
          style="padding-top: 56.25%;"
        >
          <div class="absolute top-0 left-0 w-full h-full bg-black">
            <div
              v-if="task?.video_url"
              class="w-full h-full"
            >
              <iframe 
                :src="getYouTubeEmbedUrl(task.video_url)" 
                class="w-full h-full" 
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen
              />
            </div>
            <div
              v-else
              class="w-full h-full flex items-center justify-center text-white"
            >
              <Play class="h-16 w-16 mx-auto mb-4 opacity-50" />
              <p>Vídeo não disponível</p>
            </div>
          </div>
        </div>

        <!-- Task Details -->
        <div class="p-6">
          <h2 class="text-2xl font-bold text-gray-900 mb-4">
            {{ task?.title }}
          </h2>
          
          <div class="prose max-w-none mb-8">
            <p>{{ task?.description }}</p>
            
            <div
              v-if="task?.content"
              class="mt-4"
              v-html="task.content"
            />
          </div>
          
          <!-- Task Resources -->
          <div
            v-if="resources.length > 0"
            class="mb-8"
          >
            <h3 class="text-lg font-semibold text-gray-900 mb-3">
              Recursos Adicionais
            </h3>
            <div class="space-y-2">
              <a 
                v-for="resource in resources" 
                :key="resource.id" 
                :href="resource.resource_link || resource.resource" 
                target="_blank" 
                class="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div class="p-2 bg-blue-100 text-blue-600 rounded-lg">
                  <FileText
                    v-if="resource.type === 'DOCUMENT'"
                    class="h-5 w-5"
                  />
                  <Music
                    v-else-if="resource.type === 'AUDIO'"
                    class="h-5 w-5"
                  />
                  <Video
                    v-else-if="resource.type === 'VIDEO'"
                    class="h-5 w-5"
                  />
                  <Image
                    v-else-if="resource.type === 'IMAGE'"
                    class="h-5 w-5"
                  />
                  <Link
                    v-else
                    class="h-5 w-5"
                  />
                </div>
                <div>
                  <div class="font-medium text-gray-900">{{ resource.type_display }}</div>
                  <div class="text-sm text-gray-600">{{ resource.description }}</div>
                </div>
              </a>
            </div>
          </div>
          
          <!-- Task Completion -->
          <div class="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-gray-200">
            <div class="flex items-center gap-2">
              <div
                v-if="task?.is_completed"
                class="flex items-center gap-2 text-green-600"
              >
                <CheckCircle class="h-5 w-5" />
                <span class="font-medium">Tarefa concluída</span>
              </div>
              <div
                v-else
                class="text-gray-600"
              >
                <span>Marque como concluída quando terminar esta tarefa</span>
              </div>
            </div>
            
            <button 
              :class="[
                'px-6 py-2 rounded-lg font-medium transition-colors',
                task?.is_completed 
                  ? 'bg-gray-100 text-gray-600 hover:bg-gray-200' 
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              ]" 
              @click="markTaskAsComplete"
            >
              {{ task?.is_completed ? 'Marcar como não concluída' : 'Marcar como concluída' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Navigation Buttons -->
      <div class="flex justify-between">
        <button 
          :disabled="currentTaskIndex === 0" 
          :class="[
            'flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-colors',
            currentTaskIndex === 0
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-white text-gray-700 hover:bg-gray-100'
          ]"
          @click="navigateToPreviousTask"
        >
          <ChevronLeft class="h-5 w-5" />
          Tarefa Anterior
        </button>
        
        <button 
          :disabled="currentTaskIndex === course?.tasks.length - 1" 
          :class="[
            'flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-colors',
            currentTaskIndex === course?.tasks.length - 1
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          ]"
          @click="navigateToNextTask"
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
import lessonService from '@/services/lessonService';
import { 
  ArrowLeft, 
  Play, 
  CheckCircle, 
  ChevronLeft, 
  ChevronRight,
  FileText,
  Music,
  Video,
  Image,
  Link
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

// --- ESTADO DO COMPONENTE ---
const course = ref(null);
const task = ref(null);
const resources = ref([]);
const isLoading = ref(true);
const error = ref(null);

// Função para converter URL do YouTube para formato de incorporação
const getYouTubeEmbedUrl = (url) => {
  if (!url) return null;
  
  // Se já for uma URL de incorporação, retorna como está
  if (url.includes('youtube.com/embed/')) return url;
  
  // Extrai o ID do vídeo da URL
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
  const match = url.match(regExp);
  
  return match && match[2].length === 11
    ? `https://www.youtube.com/embed/${match[2]}`
    : null;
};

const fetchTaskResources = async (taskId) => {
  try {
    const response = await lessonService.getTaskResources(taskId);
    resources.value = response.data;
  } catch (err) {
    console.error("Erro ao buscar recursos da tarefa:", err);
  }
};

const findAndSetCurrentTask = () => {
  if (!course.value) return;
  const taskId = parseInt(route.params.taskId);
  const foundTask = course.value.tasks.find(t => t.id === taskId);
  
  if (foundTask) {
    task.value = foundTask;
    fetchTaskResources(taskId); // Busca os recursos quando a tarefa é definida
  } else {
    error.value = "Tarefa não encontrada neste curso.";
    router.push(`/course/${route.params.courseId}`);
  }
};

const fetchCourseData = async () => {
  isLoading.value = true;
  error.value = null;
  task.value = null;
  course.value = null;
  
  const courseId = route.params.courseId;
  try {
    const response = await lessonService.getLessonDetail(courseId);
    course.value = response.data;
    findAndSetCurrentTask();
  } catch (err) {
    console.error("Erro ao buscar detalhes do curso:", err);
    error.value = "Não foi possível carregar o minicurso.";
  } finally {
    isLoading.value = false;
  }
};

// Observa mudanças no ID da tarefa na URL para navegar entre as tarefas sem recarregar o curso
watch(() => route.params.taskId, () => {
  if (course.value) {
    findAndSetCurrentTask();
  }
});

// --- PROPRIEDADES COMPUTADAS ---
const currentTaskIndex = computed(() => {
  if (!course.value || !task.value) return -1;
  return course.value.tasks.findIndex(t => t.id === task.value.id);
});

const courseProgress = computed(() => {
  if (!course.value?.tasks?.length) return 0;
  const completedCount = course.value.tasks.filter(t => t.is_completed).length;
  return Math.round((completedCount / course.value.tasks.length) * 100);
});

const goBackToCourse = () => {
  router.push(`/course/${route.params.courseId}`);
};

const markTaskAsComplete = async () => {
  if (!task.value) return;

  try {
    if (task.value.is_completed) {
      // Se a tarefa já está concluída, vamos desmarcá-la
      await lessonService.uncompleteTask(task.value.id);
      task.value.is_completed = false;
    } else {
      // Se a tarefa não está concluída, vamos marcá-la
      await lessonService.completeTask(task.value.id);
      task.value.is_completed = true;

      // Se houver uma próxima tarefa, navega para ela automaticamente
      if (currentTaskIndex.value < course.value.tasks.length - 1) {
        navigateToNextTask();
      } else {
        // Se for a última tarefa, mostra mensagem de conclusão
        alert("Parabéns! Você concluiu todas as tarefas deste curso!");
      }
    }

    // Atualiza o progresso do curso
    await fetchCourseData();
  } catch (err) {
    console.error("Erro ao atualizar status da tarefa:", err);
    alert("Houve um erro ao salvar seu progresso. Tente novamente.");
  }
};

const navigateToTaskById = (taskId) => {
  router.push(`/course/${route.params.courseId}/task/${taskId}`);
};

const navigateToPreviousTask = () => {
  if (currentTaskIndex.value > 0) {
    const previousTask = course.value.tasks[currentTaskIndex.value - 1];
    navigateToTaskById(previousTask.id);
  }
};

const navigateToNextTask = () => {
  if (currentTaskIndex.value < course.value.tasks.length - 1) {
    const nextTask = course.value.tasks[currentTaskIndex.value + 1];
    navigateToTaskById(nextTask.id);
  }
};

// Observa mudanças nos parâmetros da rota para recarregar os dados quando necessário
watch(() => route.params, () => {
  fetchCourseData();
}, { immediate: true });

onMounted(fetchCourseData);
</script>

<style scoped>
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