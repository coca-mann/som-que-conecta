<template>
    <div class="space-y-6">
      <h1 class="text-3xl font-bold text-emerald-800 mb-6">Mini-Cursos para Iniciantes</h1>
      
      <div v-if="!isLoggedIn" class="bg-amber-50 border border-amber-200 rounded-lg p-6 text-center">
        <LockIcon class="h-12 w-12 text-amber-500 mx-auto mb-4" />
        <h2 class="text-xl font-semibold mb-2">Acesso Restrito</h2>
        <p class="text-gray-600 mb-4">Faça login para acessar nossos mini-cursos e começar sua jornada musical.</p>
        <button 
          @click="emitOpenLoginModal"
          class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors"
        >
          Entrar
        </button>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="(course, index) in courses" 
          :key="index" 
          class="bg-white rounded-lg shadow-md overflow-hidden cursor-pointer hover:shadow-xl transition-shadow"
          @click="navigateToCourseDetail(course.id)"
        >
          <div class="h-48 bg-gradient-to-r from-emerald-500 to-teal-600 relative">
            <div class="absolute inset-0 flex items-center justify-center">
              <component :is="course.icon" class="h-20 w-20 text-white" />
            </div>
            <div class="absolute top-2 right-2 bg-white rounded-full px-2 py-1 text-xs font-medium text-emerald-700">
              {{ course.level }}
            </div>
          </div>
          <div class="p-4">
            <h3 class="text-xl font-semibold mb-2">{{ course.title }}</h3>
            <p class="text-gray-600 mb-4 text-sm">{{ course.description }}</p>
            <div class="flex items-center justify-between mb-4 text-xs text-gray-500">
              <div class="flex items-center">
                <ClockIcon class="h-4 w-4 mr-1" />
                <span>{{ course.duration }}</span>
              </div>
              <div class="flex items-center">
                <UsersIcon class="h-4 w-4 mr-1" />
                <span>{{ course.students }} alunos</span>
              </div>
            </div>
            
            <div v-if="course.enrolled" class="mb-4">
              <div class="flex justify-between text-sm mb-1">
                <span>Progresso</span>
                <span>{{ course.progress }}%</span>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2.5">
                <div class="bg-emerald-600 h-2.5 rounded-full" :style="{ width: course.progress + '%' }"></div>
              </div>
            </div>
            
            <button class="w-full py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
              {{ course.enrolled ? 'Continuar' : 'Iniciar Curso' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, defineProps, getCurrentInstance } from 'vue';
  import { useRouter } from 'vue-router';
  import { 
    Lock as LockIcon,
    Clock as ClockIcon,
    Users as UsersIcon,
    Guitar as GuitarIcon,
    Piano as PianoIcon,
    Drum as DrumIcon,
    Mic as MicIcon
  } from 'lucide-vue-next';
  
  const props = defineProps({
    isLoggedIn: Boolean
  });
  
  const instance = getCurrentInstance();
  const emitOpenLoginModal = () => {
    instance.emit('openLoginModal');
  };
  
  const router = useRouter();
  
  const courses = ref([
    {
      id: 'violao-iniciante', // Adicione IDs únicos
      title: 'Violão para Iniciantes',
      description: 'Aprenda os acordes básicos e comece a tocar suas músicas favoritas.',
      level: 'Iniciante',
      duration: '4 semanas',
      students: 1245,
      icon: GuitarIcon,
      enrolled: true, // Simule quais cursos o usuário está inscrito
      progress: 65,
    },
    {
      id: 'piano-fundamentos',
      title: 'Fundamentos do Piano',
      description: 'Domine as técnicas básicas do piano e leitura de partituras.',
      level: 'Iniciante',
      duration: '6 semanas',
      students: 890,
      icon: PianoIcon,
      enrolled: true,
      progress: 30,
    },
    {
      id: 'bateria-intro',
      title: 'Introdução à Bateria',
      description: 'Aprenda ritmos básicos e técnicas de coordenação na bateria.',
      level: 'Iniciante',
      duration: '5 semanas',
      students: 723,
      icon: DrumIcon,
      enrolled: false,
      progress: 0,
    },
    {
      id: 'canto-iniciantes',
      title: 'Canto para Iniciantes',
      description: 'Desenvolva sua voz e aprenda técnicas vocais fundamentais.',
      level: 'Iniciante',
      duration: '8 semanas',
      students: 1056,
      icon: MicIcon,
      enrolled: false,
      progress: 0,
    }
  ]);
  
  const navigateToCourseDetail = (courseId) => {
    router.push({ name: 'CourseDetail', params: { courseId } });
  };
  </script>