<template>
    <div v-if="loading" class="text-center py-10">Carregando detalhes do curso...</div>
    <div v-else-if="!selectedCourse" class="text-center py-10 text-red-500">Curso não encontrado.</div>
    <div v-else class="space-y-6">
      <div class="flex items-center mb-6">
        <router-link 
          to="/cursos"
          class="mr-4 p-2 rounded-full hover:bg-gray-100"
        >
          <ArrowLeftIcon class="h-5 w-5 text-gray-700" />
        </router-link>
        <h1 class="text-3xl font-bold text-emerald-800">{{ selectedCourse.title }}</h1>
      </div>
      
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="h-64 bg-gradient-to-r from-emerald-500 to-teal-600 relative">
          <div class="absolute inset-0 flex items-center justify-center">
            <component :is="selectedCourse.icon" class="h-32 w-32 text-white" />
          </div>
        </div>
        
        <div class="p-6">
          <div class="flex flex-wrap gap-2 mb-4">
            <span class="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full text-sm">
              {{ selectedCourse.level }}
            </span>
            <span class="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm flex items-center">
              <ClockIcon class="h-4 w-4 mr-1" />
              {{ selectedCourse.duration }}
            </span>
            <span class="px-3 py-1 bg-gray-100 text-gray-800 rounded-full text-sm flex items-center">
              <UsersIcon class="h-4 w-4 mr-1" />
              {{ selectedCourse.students }} alunos
            </span>
          </div>
          
          <p class="text-gray-600 mb-6">{{ selectedCourse.fullDescription || selectedCourse.description }}</p>
          
          <div class="mb-6">
            <div class="flex justify-between text-sm mb-1">
              <span class="font-medium">Seu progresso</span>
              <span>{{ selectedCourse.progress }}%</span>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2.5">
              <div class="bg-emerald-600 h-2.5 rounded-full" :style="{ width: selectedCourse.progress + '%' }"></div>
            </div>
          </div>
          
          <div class="space-y-4">
            <h2 class="text-xl font-semibold">Lições</h2>
            <div v-if="!selectedCourse.lessons || selectedCourse.lessons.length === 0" class="text-gray-500">
              Nenhuma lição disponível para este curso ainda.
            </div>
            <div v-else v-for="(lesson, index) in selectedCourse.lessons" :key="index" class="border rounded-lg overflow-hidden">
              <div 
                class="flex items-center justify-between p-4 cursor-pointer"
                :class="{'bg-gray-50': lesson.completed}"
                @click="toggleLesson(lesson)"
              >
                <div class="flex items-center">
                  <div 
                    class="w-8 h-8 rounded-full flex items-center justify-center mr-3"
                    :class="lesson.completed ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-500'"
                  >
                    <CheckIcon v-if="lesson.completed" class="h-5 w-5" />
                    <span v-else>{{ index + 1 }}</span>
                  </div>
                  <div>
                    <h3 class="font-medium">{{ lesson.title }}</h3>
                    <p class="text-sm text-gray-500">{{ lesson.duration }}</p>
                  </div>
                </div>
                <ChevronDownIcon 
                  class="h-5 w-5 text-gray-400 transition-transform"
                  :class="{'transform rotate-180': lesson.expanded}"
                />
              </div>
              
              <div v-if="lesson.expanded" class="p-4 border-t">
                <p class="text-gray-600 mb-4">{{ lesson.description }}</p>
                
                <div v-if="lesson.videoUrl" class="bg-gray-100 aspect-video mb-4 flex items-center justify-center">
                  <PlayIcon class="h-12 w-12 text-gray-400" />
                   <p class="ml-2 text-gray-500">Simulação de player de vídeo</p>
                </div>
                
                <div class="flex justify-between items-center">
                  <button 
                    v-if="!lesson.completed" 
                    @click="completeLesson(lesson)"
                    class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors"
                  >
                    Marcar como Concluída
                  </button>
                  <button 
                    v-else
                    class="px-4 py-2 bg-gray-200 text-gray-700 rounded-md cursor-not-allowed"
                    disabled
                  >
                    Lição Concluída
                  </button>
                  
                  <button 
                    v-if="index < selectedCourse.lessons.length - 1 && lesson.completed"
                    @click="goToNextLesson(index)"
                    class="px-4 py-2 bg-emerald-100 text-emerald-700 rounded-md hover:bg-emerald-200 transition-colors"
                  >
                    Próxima Lição
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import { useRoute } from 'vue-router';
  import { 
    ArrowLeftIcon, 
    ClockIcon, 
    UsersIcon, 
    CheckIcon, 
    ChevronDownIcon, 
    PlayIcon,
    Guitar as GuitarIcon, // Exemplo de ícones de curso
    Piano as PianoIcon,
    Drum as DrumIcon,
    Mic as MicIcon
  } from 'lucide-vue-next';
  
  const props = defineProps({
    courseId: String, // Recebido do router (props: true na definição da rota)
    isLoggedIn: Boolean // Recebido do App.vue
  });
  
  const route = useRoute();
  const loading = ref(true);
  const selectedCourse = ref(null);
  
  // Dados mockados de cursos (deveriam vir de um store ou API)
  // Adicione mais detalhes e lições aqui
  const allCoursesData = ref([
    {
      id: 'violao-iniciante',
      title: 'Violão para Iniciantes',
      description: 'Aprenda os acordes básicos e comece a tocar suas músicas favoritas.',
      fullDescription: 'Este curso abrange desde a postura correta e partes do violão, até os primeiros acordes e ritmos, permitindo que você toque suas primeiras músicas em poucas semanas.',
      level: 'Iniciante',
      duration: '4 semanas',
      students: 1245,
      icon: GuitarIcon,
      progress: 65, // O progresso do usuário neste curso
      lessons: [
        { id: 'v1', title: 'Introdução ao Violão', duration: '15 min', description: 'Conheça as partes do violão e aprenda a postura correta para tocar.', videoUrl: 'sim', completed: true, expanded: false },
        { id: 'v2', title: 'Primeiros Acordes: Dó, Sol, Ré', duration: '20 min', description: 'Aprenda os acordes básicos: Dó (C), Sol (G) e Ré (D).', videoUrl: 'sim', completed: true, expanded: false },
        { id: 'v3', title: 'Ritmos Básicos e Batidas', duration: '25 min', description: 'Pratique ritmos simples para acompanhar músicas populares.', videoUrl: 'sim', completed: false, expanded: false },
        { id: 'v4', title: 'Sua Primeira Música Completa', duration: '30 min', description: 'Aprenda a tocar uma música completa usando os acordes e ritmos aprendidos.', videoUrl: 'sim', completed: false, expanded: false }
      ]
    },
    {
      id: 'piano-fundamentos',
      title: 'Fundamentos do Piano',
      description: 'Domine as técnicas básicas do piano e leitura de partituras.',
      fullDescription: 'Explore o teclado, aprenda as notas musicais, formação de acordes simples e comece a ler partituras de nível iniciante.',
      level: 'Iniciante',
      duration: '6 semanas',
      students: 890,
      icon: PianoIcon,
      progress: 30,
      lessons: [
          { id: 'p1', title: 'Conhecendo o Teclado', duration: '20 min', description: 'Identificação das notas, oitavas e teclas pretas.', videoUrl: 'sim', completed: true, expanded: false },
          { id: 'p2', title: 'Leitura de Partitura Básica', duration: '30 min', description: 'Clave de Sol, clave de Fá e valores das notas.', videoUrl: 'sim', completed: false, expanded: false },
      ]
    },
      {
      id: 'bateria-intro',
      title: 'Introdução à Bateria',
      description: 'Aprenda ritmos básicos e técnicas de coordenação na bateria.',
      level: 'Iniciante',
      duration: '5 semanas',
      students: 723,
      icon: DrumIcon,
      progress: 0,
      lessons: [] // Adicionar lições se desejar
    },
    {
      id: 'canto-iniciantes',
      title: 'Canto para Iniciantes',
      description: 'Desenvolva sua voz e aprenda técnicas vocais fundamentais.',
      level: 'Iniciante',
      duration: '8 semanas',
      students: 1056,
      icon: MicIcon,
      progress: 0,
      lessons: [] // Adicionar lições se desejar
    }
  ]);
  
  onMounted(() => {
    const courseIdFromRoute = props.courseId || route.params.courseId;
    // Simula busca de dados
    setTimeout(() => {
      selectedCourse.value = allCoursesData.value.find(c => c.id === courseIdFromRoute) || null;
      if (selectedCourse.value && selectedCourse.value.lessons) {
          selectedCourse.value.lessons = selectedCourse.value.lessons.map(l => ({...l, expanded: false}));
      }
      loading.value = false;
    }, 500);
  });
  
  const toggleLesson = (lesson) => {
    lesson.expanded = !lesson.expanded;
  };
  
  const completeLesson = (lessonToComplete) => {
    if (selectedCourse.value && selectedCourse.value.lessons) {
      const lesson = selectedCourse.value.lessons.find(l => l.id === lessonToComplete.id);
      if (lesson) {
        lesson.completed = true;
        updateCourseProgress();
      }
    }
  };
  
  const updateCourseProgress = () => {
    if (selectedCourse.value && selectedCourse.value.lessons && selectedCourse.value.lessons.length > 0) {
      const totalLessons = selectedCourse.value.lessons.length;
      const completedLessons = selectedCourse.value.lessons.filter(l => l.completed).length;
      selectedCourse.value.progress = Math.round((completedLessons / totalLessons) * 100);
    } else if (selectedCourse.value) {
       selectedCourse.value.progress = 0;
    }
  };
  
  const goToNextLesson = (currentIndex) => {
    if (selectedCourse.value && selectedCourse.value.lessons) {
      // Fecha a atual
      if(selectedCourse.value.lessons[currentIndex]) {
          selectedCourse.value.lessons[currentIndex].expanded = false;
      }
      // Abre a próxima se existir
      if (currentIndex < selectedCourse.value.lessons.length - 1) {
        const nextLesson = selectedCourse.value.lessons[currentIndex + 1];
        if(nextLesson) {
            nextLesson.expanded = true;
            // Opcional: rolar para a próxima lição se a página for longa
            // const lessonElement = document.getElementById(`lesson-${nextLesson.id}`); // Supondo que você adicione IDs aos elementos da lição
            // if (lessonElement) lessonElement.scrollIntoView({ behavior: 'smooth' });
        }
      }
    }
  };
  </script>