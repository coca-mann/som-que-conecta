<template>
    <div class="space-y-8">
      <h1 class="text-3xl font-bold text-emerald-800 mb-6">Instrumentos Musicais</h1>
      
      <div v-if="!isLoggedIn" class="bg-amber-50 border border-amber-200 rounded-lg p-6 text-center">
        <LockIcon class="h-12 w-12 text-amber-500 mx-auto mb-4" />
        <h2 class="text-xl font-semibold mb-2">Acesso Restrito</h2>
        <p class="text-gray-600 mb-4">Faça login para acessar informações sobre instrumentos disponíveis e gerenciar seus instrumentos.</p>
        <button 
          @click="emitOpenLoginModal"
          class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors"
        >
          Entrar
        </button>
      </div>
      
      <div v-else>
        <section>
          <h2 class="text-2xl font-semibold mb-4">Seus Instrumentos (Aluno)</h2>
          <div v-if="userType === 'student'">
              <div v-if="myInstruments.length === 0" class="bg-gray-100 rounded-lg p-6 text-center">
                  <MusicIcon class="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p class="text-gray-600">Você ainda não possui instrumentos registrados.</p>
              </div>
              <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                  <div v-for="(instrument, index) in myInstruments" :key="index" class="bg-white rounded-lg shadow-md p-4">
                  <div class="h-40 bg-gray-100 rounded-md flex items-center justify-center mb-3">
                      <component :is="instrument.icon" class="h-16 w-16 text-emerald-600" />
                  </div>
                  <h3 class="font-semibold">{{ instrument.name }}</h3>
                  <p class="text-sm text-gray-500">Adicionado em {{ instrument.addedDate }}</p>
                  </div>
              </div>
          </div>
           <div v-else class="text-gray-600 bg-gray-100 p-4 rounded-md">
              <p>Voluntários gerenciam instrumentos na seção "Gerenciar Instrumentos".</p>
          </div>
        </section>
  
        <section class="mt-8">
          <h2 class="text-2xl font-semibold mb-4">Instrumentos Disponíveis (Comunidade)</h2>
          <div class="bg-white rounded-lg shadow-md p-4">
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-1">Filtrar por:</label>
              <div class="flex flex-wrap gap-2">
                <button 
                  v-for="(source, index) in ['Todos', 'ONGs', 'Professores']" 
                  :key="index"
                  :class="{'bg-emerald-600 text-white': instrumentFilter === source, 'bg-gray-100 text-gray-800': instrumentFilter !== source}"
                  class="px-3 py-1 rounded-md text-sm"
                  @click="instrumentFilter = source"
                >
                  {{ source }}
                </button>
              </div>
            </div>
            
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div 
                v-for="(instrument, index) in filteredAvailableInstruments" 
                :key="index" 
                class="bg-gray-50 rounded-lg p-4 border border-gray-200"
              >
                <div class="flex items-center mb-3">
                  <component :is="instrument.icon" class="h-8 w-8 text-emerald-600 mr-2" />
                  <h3 class="font-semibold">{{ instrument.name }}</h3>
                </div>
                <p class="text-sm text-gray-600 mb-2">{{ instrument.description }}</p>
                <div class="flex justify-between items-center">
                  <span class="text-xs px-2 py-1 bg-emerald-100 text-emerald-800 rounded-full">{{ instrument.source }}</span>
                  <router-link 
                      :to="`/instrumentos/${instrument.id}/agenda`" 
                                      class="text-sm text-emerald-600 hover:text-emerald-500"
                                  >
                    Ver Disponibilidade
                  </router-link>
                </div>
              </div>
               <div v-if="filteredAvailableInstruments.length === 0" class="col-span-full text-center text-gray-500 py-4">
                  Nenhum instrumento encontrado para este filtro.
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, defineProps, getCurrentInstance } from 'vue';
  import { 
    Music as MusicIcon,
    Lock as LockIcon,
    Guitar as GuitarIcon,
    Piano as PianoIcon,
    Drum as DrumIcon,
    Mic as MicIcon
  } from 'lucide-vue-next';
  
  // Props recebidas do App.vue
  const props = defineProps({
    isLoggedIn: Boolean,
    userType: String
  });
  
  // Emitir evento para App.vue abrir o modal de login
  const instance = getCurrentInstance();
  const emitOpenLoginModal = () => {
    instance.emit('openLoginModal');
  };
  
  
  const instrumentFilter = ref('Todos');
  
  // Dados que eram globais, agora são locais para esta página
  const myInstruments = ref([ // Instrumentos do aluno logado
    {
      name: 'Violão Acústico',
      addedDate: '10/04/2024',
      icon: GuitarIcon
    }
  ]);
  
  const availableInstruments = ref([ // Instrumentos da comunidade
    {
      id: 'violao1', // Adicione IDs únicos
      name: 'Violão Clássico',
      description: 'Violão para iniciantes em bom estado.',
      source: 'ONGs',
      icon: GuitarIcon
    },
    {
      id: 'piano1',
      name: 'Piano Digital',
      description: 'Piano digital com 88 teclas, ideal para estudantes.',
      source: 'Professores',
      icon: PianoIcon
    },
    {
      id: 'flauta1',
      name: 'Flauta Doce',
      description: 'Flauta doce soprano, perfeita para iniciantes.',
      source: 'ONGs',
      icon: MusicIcon // Ícone genérico de música para flauta
    },
    {
      id: 'ukulele1',
      name: 'Ukulele',
      description: 'Ukulele soprano em ótimo estado.',
      source: 'Professores',
      icon: GuitarIcon
    },
    {
      id: 'bateria1',
      name: 'Bateria Eletrônica',
      description: 'Bateria eletrônica para prática silenciosa.',
      source: 'Professores',
      icon: DrumIcon
    },
    {
      id: 'mic1',
      name: 'Microfone',
      description: 'Microfone dinâmico para aulas de canto.',
      source: 'ONGs',
      icon: MicIcon
    }
  ]);
  
  const filteredAvailableInstruments = computed(() => {
    if (instrumentFilter.value === 'Todos') {
      return availableInstruments.value;
    }
    return availableInstruments.value.filter(instrument => instrument.source === instrumentFilter.value);
  });
  </script>