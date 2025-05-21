<template>
    <div class="space-y-6">
      <h1 class="text-3xl font-bold text-emerald-800 mb-6">Gerenciar Seus Instrumentos</h1>
  
      <div v-if="!isLoggedIn || userType !== 'volunteer'" class="bg-amber-50 border border-amber-200 rounded-lg p-6 text-center">
        <LockIcon class="h-12 w-12 text-amber-500 mx-auto mb-4" />
        <h2 class="text-xl font-semibold mb-2">Acesso Restrito</h2>
        <p class="text-gray-600 mb-4">Esta área é exclusiva para ONGs e professores voluntários.</p>
        <button v-if="!isLoggedIn" @click="emitOpenLoginModal" class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
          Entrar como Voluntário
        </button>
         <p v-else class="text-gray-600">Por favor, acesse com uma conta de voluntário.</p>
      </div>
      
      <div v-else>
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold">Seus Instrumentos Disponibilizados</h2>
            <button 
              @click="triggerAddInstrumentModal"
              class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors flex items-center"
            >
              <PlusCircleIcon class="h-5 w-5 mr-2"/> Adicionar Instrumento
            </button>
          </div>
          
          <div v-if="volunteerInstruments.length === 0" class="text-center text-gray-500 py-6">
              Você ainda não adicionou nenhum instrumento.
          </div>
          <div v-else class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Instrumento</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Reservas</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Ações</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(instrument, index) in volunteerInstruments" :key="instrument.id || index">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="bg-emerald-100 p-2 rounded-md mr-3">
                        <component :is="instrument.icon" class="h-5 w-5 text-emerald-600" />
                      </div>
                      <div>
                        <div class="font-medium">{{ instrument.name }}</div>
                        <div class="text-sm text-gray-500">{{ instrument.description }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span 
                      class="px-2 py-1 text-xs rounded-full"
                      :class="instrument.available ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                    >
                      {{ instrument.available ? 'Disponível' : 'Indisponível' }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ instrument.bookings }} reservas</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm">
                    <button class="text-emerald-600 hover:text-emerald-500 mr-3">Editar</button>
                    <button class="text-red-600 hover:text-red-500">Remover</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, defineProps, getCurrentInstance } from 'vue';
  import { 
      Lock as LockIcon, 
      PlusCircleIcon,
      Guitar as GuitarIcon, // Exemplo de ícones de instrumento
      Music as MusicIcon 
  } from 'lucide-vue-next';
  
  const props = defineProps({
    isLoggedIn: Boolean,
    userType: String // 'student' or 'volunteer'
  });
  
  const instance = getCurrentInstance();
  const emitOpenLoginModal = () => {
    instance.emit('openLoginModal');
  };
  const triggerAddInstrumentModal = () => {
    instance.emit('openAddInstrumentModal'); // Evento para App.vue
  };
  
  // Mock data (instrumentos que o voluntário/ONG cadastrou)
  const volunteerInstruments = ref([
    {
      id: 'vol-violao1',
      name: 'Violão Clássico (doado)',
      description: 'Violão para iniciantes em bom estado.',
      icon: GuitarIcon,
      available: true,
      bookings: 5
    },
    {
      id: 'vol-flauta1',
      name: 'Flauta Doce (Prof. Silva)',
      description: 'Flauta doce soprano, perfeita para iniciantes.',
      icon: MusicIcon,
      available: false, // Exemplo de indisponível
      bookings: 2
    }
  ]);
  
  // Lógica para adicionar/editar/remover instrumentos iria aqui,
  // interagindo com o backend e atualizando `volunteerInstruments`.
  // O modal de "Adicionar" está no App.vue, então após adicionar, App.vue
  // precisaria de uma forma de notificar esta página para recarregar/atualizar
  // a lista (ou usar Pinia para reatividade automática).
  </script>