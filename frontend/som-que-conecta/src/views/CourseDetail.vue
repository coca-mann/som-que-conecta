<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto px-0 sm:px-6 lg:px-8 py-8">
      <div
        v-if="course"
        class="bg-white rounded-lg shadow-lg overflow-hidden"
      >
        <div class="bg-gradient-to-r from-red-600 to-red-800 text-white p-8">
          <div class="flex items-start justify-between">
            <div>
              <h1 class="text-3xl font-bold mb-2">
                {{ course.title }}
              </h1>
              <p class="text-red-100 mb-4">
                {{ course.description }}
              </p>
              <div class="flex items-center gap-4 text-sm">
                <span class="flex items-center gap-1">
                  <Clock class="h-4 w-4" />
                  {{ formatDuration(course.time_to_complete, course.type_time_to_complete) }}
                </span>
                <span class="flex items-center gap-1">
                  <BookOpen class="h-4 w-4" />
                  {{ course.tasks_count }} aulas
                </span>
                <span class="flex items-center gap-1">
                  <User class="h-4 w-4" />
                  {{ course.author }}
                </span>
              </div>
            </div>
            <button
              class="text-white hover:text-red-200 transition-colors"
              @click="$router.push('/courses')"
            >
              <X class="h-6 w-6" />
            </button>
          </div>
        </div>

        <div class="p-6 border-b">
          <div class="flex justify-between items-center mb-2">
            <h3 class="text-lg font-semibold">
              Seu Progresso
            </h3>
            <span class="text-2xl font-bold text-red-600">{{ progressPercentage }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-3">
            <div
              class="bg-red-600 h-3 rounded-full transition-all duration-500"
              :style="{ width: progressPercentage + '%' }"
            />
          </div>
          <p class="text-sm text-gray-600 mt-2">
            {{ completedTasks }} de {{ course.tasks.length }} tarefas concluídas
          </p>
        </div>

        <div class="p-6">
          <h3 class="text-xl font-semibold mb-6">
            Tarefas do Curso
          </h3>
          <div class="space-y-4">
            <div
              v-for="(task, index) in orderedTasks"
              :key="task.id"
              class="border rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-4">
                  <div class="flex-shrink-0">
                    <div
                      :class="[
                        'w-8 h-8 rounded-full flex items-center justify-center font-bold', // Estilo base do número
                        task.is_completed ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
                      ]"
                    >
                      {{ index + 1 }}
                    </div>
                  </div>
                  <div>
                    <h4
                      :class="[
                        'font-medium',
                        task.is_completed ? 'text-green-800 line-through' : 'text-gray-900' // Texto riscado se concluído
                      ]"
                    >
                      {{ task.title }}
                    </h4>
                    <p
                      v-if="task.description"
                      class="text-sm text-gray-600 mt-1"
                    >
                      {{ task.description }}
                    </p>
                  </div>
                </div>
                
                <div class="flex items-center gap-2">
                  <button 
                    v-if="task.is_completed"
                    class="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium"
                    disabled
                  >
                    <Check class="h-4 w-4 inline mr-1" />
                    Concluída
                  </button>
                  <button 
                    class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm"
                    @click="goToTask(task)"
                  >
                    {{ task.is_completed ? 'Revisar' : 'Iniciar' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

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
                class="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                @click="continueFromLastTask"
              >
                Continuar Estudando
              </button>
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="showCompletionModal"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      >
        <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
          <div class="text-center">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Check class="h-8 w-8 text-green-600" />
            </div>
            <h3 class="text-lg font-semibold mb-2">
              Tarefa Concluída!
            </h3>
            <p class="text-gray-600 mb-4">
              Parabéns! Você completou mais uma etapa do seu aprendizado.
            </p>
            <button 
              class="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              @click="showCompletionModal = false"
            >
              Continuar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store';
import lessonService from '@/services/lessonService';
import { Clock, BookOpen, User, X, Check, Award } from 'lucide-vue-next'
import { useHead } from '@vueuse/head';

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore();

// --- ESTADO DO COMPONENTE ---
const course = ref(null);
const isLoading = ref(true);
const error = ref(null);
const showCompletionModal = ref(false);

// --- LÓGICA DE DADOS ---
const fetchCourseDetail = async () => {
  isLoading.value = true;
  error.value = null;
  const courseId = route.params.id;

  try {
    const response = await lessonService.getLessonDetail(courseId);
    course.value = response.data;
  } catch (err) {
    console.error("Erro ao buscar detalhes do curso:", err);
    error.value = "Minicurso não encontrado.";
    // Opcional: redirecionar para uma página 404
  } finally {
    isLoading.value = false;
  }
};

watch(course, (newCourse) => {
  if (newCourse) {
    useHead({
      title: `${newCourse.title} | Som que Conecta`,
      meta: [
        { name: 'description', content: newCourse.description },
      ],
    })
  }
})

// --- PROPRIEDADES COMPUTADAS ---
const orderedTasks = computed(() => {
  if (!course.value?.tasks) return [];
  // Ordena pelo campo 'order' de forma ascendente
  return [...course.value.tasks].sort((a, b) => a.order - b.order);
});

const completedTasks = computed(() => {
  // A API agora envia 'is_completed' para cada tarefa
  return orderedTasks.value.filter(task => task.is_completed).length || 0;
});

const progressPercentage = computed(() => {
  if (!orderedTasks.value.length) return 0;
  return Math.round((completedTasks.value / orderedTasks.value.length) * 100);
});

// --- MÉTODOS ---
const goToTask = (task) => {
  router.push(`/course/${course.value.id}/task/${task.id}`);
};

const continueFromLastTask = () => {
  // Encontra a primeira tarefa não completada
  const nextTask = orderedTasks.value.find(task => !task.is_completed);
  
  if (nextTask) {
    goToTask(nextTask);
  } else if (orderedTasks.value.length > 0) {
    // Se todas estiverem completas, vai para a primeira
    goToTask(orderedTasks.value[0]);
  }
};

const formatDuration = (time, type) => {
    if (!time || !type) return '';
    const typeMap = { 'D': 'dias', 'M': 'meses', 'Y': 'anos' };
    const plural = time > 1 ? typeMap[type] || type : (typeMap[type] || type).slice(0, -1);
    return `${time} ${plural}`;
}

onMounted(() => {
  window.scrollTo(0, 0);
  fetchCourseDetail();
});
</script>