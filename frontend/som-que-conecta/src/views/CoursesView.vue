<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Minicursos</h1>
      <p class="text-gray-600">Aprenda música passo a passo com nossos cursos estruturados gratuitos</p>
    </div>

    <!-- Mensagem de Login -->
    <div v-if="!isLoggedIn" class="mb-8 bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
      <h2 class="text-xl font-semibold text-blue-900 mb-2">Faça login para acessar os minicursos</h2>
      <p class="text-blue-700 mb-4">Para iniciar ou continuar seus estudos, você precisa estar logado em sua conta.</p>
      <router-link 
        to="/auth?redirect=/courses" 
        class="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
      >
        Fazer Login
      </router-link>
    </div>

    <!-- Filters -->
    <div v-if="isLoggedIn" class="mb-8 flex flex-wrap gap-4">
      <select v-model="selectedLevel" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option value="">Todos os Níveis</option>
        <option v-for="level in skillLevels" :key="level.value" :value="level.value">
          {{ level.label }}
        </option>
      </select>
      
      <select v-model="selectedInstrument" class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        <option value="">Todos os Instrumentos</option>
        <option v-for="instrument in instrumentTypes" :key="instrument.value" :value="instrument.value">
          {{ instrument.label }}
        </option>
      </select>
    </div>

    <!-- Courses Grid -->
    <div v-if="isLoggedIn" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="course in courses" :key="course.id" class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
        <img :src="course.cover" :alt="course.title" class="w-full h-48 object-cover">
        
        <div class="p-6">
          <div class="flex items-center gap-2 mb-2">
            <span class="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded-full">{{ course.skill_level_display }}</span>
            <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">{{ course.instrument_type_name }}</span>
          </div>
          
          <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ course.title }}</h3>
          <p class="text-gray-600 mb-4">{{ course.description }}</p>
          
          <div class="space-y-2 mb-4">
            <div class="flex items-center justify-between text-sm text-gray-600">
              <div class="flex items-center gap-2">
                <Clock class="h-4 w-4" />
                <span>{{ course.duration_display }}</span>
              </div>
              <div class="flex items-center gap-2">
                <BookOpen class="h-4 w-4" />
                <span>{{ course.tasks_count }} aulas</span>
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
import { ref, computed, onMounted, watch } from 'vue'
import { Clock, BookOpen } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store';
import lessonService from '@/services/lessonService';

const router = useRouter()
const authStore = useAuthStore();

// --- ESTADO ---
const courses = ref([]);
const isLoading = ref(true);
const isLoggedIn = computed(() => authStore.isAuthenticated);

const selectedLevel = ref('')
const selectedInstrument = ref('')
const skillLevels = ref([])
const instrumentTypes = ref([])

// --- LÓGICA DE DADOS ---
const fetchSkillLevels = async () => {
  try {
    const response = await lessonService.getSkillLevels();
    skillLevels.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar níveis de habilidade:", error);
  }
};

const fetchInstrumentTypes = async () => {
  try {
    const response = await lessonService.getInstrumentTypes();
    instrumentTypes.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar tipos de instrumentos:", error);
  }
};

const fetchLessons = async () => {
  isLoading.value = true;
  
  // Monta os parâmetros de filtro para a API
  const params = {
    skill_level: selectedLevel.value,
    instrument_type: selectedInstrument.value,
  };

  try {
    const response = await lessonService.getLessons(params);
    courses.value = response.data;
  } catch (error) {
    console.error("Erro ao buscar os minicursos:", error);
  } finally {
    isLoading.value = false;
  }
};

// Observa mudanças nos filtros e busca os dados novamente
watch([selectedLevel, selectedInstrument], () => {
  if (isLoggedIn.value) {
    fetchLessons();
  }
});

// Watcher para carregar dados quando o usuário fizer login
watch(isLoggedIn, async (newValue) => {
  if (newValue) {
    console.log('Usuário autenticado. Carregando dados dos minicursos.');
    await Promise.all([
      fetchSkillLevels(),
      fetchInstrumentTypes(),
      fetchLessons()
    ]);
  }
});

// Busca inicial quando o componente é montado
onMounted(() => {
  if (isLoggedIn.value) {
    fetchSkillLevels();
    fetchInstrumentTypes();
    fetchLessons();
  }
});

// --- MÉTODOS ---
const accessCourse = (course) => {
  router.push(`/course/${course.id}`);
};

const formatDuration = (time, type) => {
    if (!time || !type) return '';
    const typeMap = { 'D': 'dias', 'M': 'meses', 'Y': 'anos' };
    const plural = time > 1 ? typeMap[type] : typeMap[type].slice(0, -1);
    return `${time} ${plural}`;
}

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
</script>