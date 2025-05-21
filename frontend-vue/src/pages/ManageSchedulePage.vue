<template>
    <div class="space-y-6">
      <h1 class="text-3xl font-bold text-emerald-800 mb-6">Gerenciar Sua Agenda de Disponibilidade</h1>
  
      <div v-if="!isLoggedIn || userType !== 'volunteer'" class="bg-amber-50 border border-amber-200 rounded-lg p-6 text-center">
        <LockIcon class="h-12 w-12 text-amber-500 mx-auto mb-4" />
        <h2 class="text-xl font-semibold mb-2">Acesso Restrito</h2>
        <p class="text-gray-600 mb-4">Esta área é exclusiva para ONGs e professores voluntários.</p>
        <button v-if="!isLoggedIn" @click="emitOpenLoginModal" class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
          Entrar como Voluntário
        </button>
      </div>
      
      <div v-else>
        <div class="bg-white rounded-lg shadow-md p-6 mb-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold">Sua Disponibilidade Semanal</h2>
            <button class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors flex items-center">
              <CalendarPlusIcon class="h-5 w-5 mr-2" /> Adicionar Novo Horário
            </button>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                  <h3 class="font-medium mb-3 text-lg">Definir Horários</h3>
                   <div class="mb-4">
                      <label class="block text-sm font-medium text-gray-700 mb-1">Selecione o Instrumento</label>
                      <select class="w-full px-3 py-2 border border-gray-300 rounded-md">
                          <option v-for="inst in managedInstrumentsForSelect" :key="inst.id" :value="inst.id">{{ inst.name }}</option>
                      </select>
                  </div>
                  <div class="mb-4">
                      <label class="block text-sm font-medium text-gray-700 mb-1">Dia da Semana</label>
                      <select class="w-full px-3 py-2 border border-gray-300 rounded-md">
                          <option v-for="day in weekDays" :key="day" :value="day">{{ day }}</option>
                      </select>
                  </div>
                   <div class="mb-4">
                      <label class="block text-sm font-medium text-gray-700 mb-1">Horário Início</label>
                      <input type="time" class="w-full px-3 py-2 border border-gray-300 rounded-md" />
                  </div>
                   <div class="mb-4">
                      <label class="block text-sm font-medium text-gray-700 mb-1">Horário Fim</label>
                      <input type="time" class="w-full px-3 py-2 border border-gray-300 rounded-md" />
                  </div>
                  <button class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">Salvar Disponibilidade</button>
              </div>
              <div>
                  <h3 class="font-medium mb-3 text-lg">Horários Definidos</h3>
                  <div v-if="volunteerSchedule.length === 0" class="text-gray-500">Nenhum horário de disponibilidade definido.</div>
                  <div v-else class="space-y-3 max-h-96 overflow-y-auto">
                  <div v-for="(slot, index) in volunteerSchedule" :key="index" class="flex items-center justify-between p-3 border rounded-md bg-gray-50">
                      <div>
                      <span class="font-medium">{{ slot.day }} - {{ slot.time }}</span>
                      <span class="text-sm text-gray-600 ml-2 block md:inline">({{ slot.instrument }})</span>
                      </div>
                      <div class="flex items-center">
                      <span 
                          class="px-2 py-1 text-xs rounded-full mr-3"
                          :class="slot.booked ? 'bg-amber-100 text-amber-800' : 'bg-green-100 text-green-800'"
                      >
                          {{ slot.booked ? 'Reservado' : 'Disponível' }}
                      </span>
                      <button class="text-red-500 hover:text-red-700">
                          <XIcon class="h-5 w-5" />
                      </button>
                      </div>
                  </div>
                  </div>
              </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6">
          <h2 class="text-xl font-semibold mb-4">Próximas Reservas Confirmadas</h2>
          <div v-if="upcomingBookings.length === 0" class="text-center text-gray-500 py-6">
              Nenhuma reserva confirmada.
          </div>
          <div v-else class="space-y-4">
            <div v-for="(booking, index) in upcomingBookings" :key="index" class="border rounded-md p-4 hover:bg-gray-50">
              <div class="flex flex-col sm:flex-row justify-between">
                <div>
                  <h3 class="font-medium text-emerald-700">{{ booking.student }}</h3>
                  <p class="text-sm text-gray-600">{{ booking.instrument }}</p>
                </div>
                <div class="text-left sm:text-right mt-2 sm:mt-0">
                  <p class="font-medium">{{ booking.date }}</p>
                  <p class="text-sm text-gray-500">{{ booking.time }}</p>
                </div>
              </div>
              <div class="flex justify-end mt-3 space-x-2">
                <button class="text-xs px-3 py-1 border border-red-500 text-red-500 rounded hover:bg-red-50">Cancelar</button>
                <button class="text-xs px-3 py-1 bg-emerald-500 text-white rounded hover:bg-emerald-600">Detalhes</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, defineProps, getCurrentInstance } from 'vue';
  import { 
      Lock as LockIcon, 
      XIcon,
      CalendarPlusIcon,
      Guitar as GuitarIcon, // Ícone para instrumento
      Music as MusicIcon // Ícone para instrumento
  } from 'lucide-vue-next';
  
  const props = defineProps({
    isLoggedIn: Boolean,
    userType: String
  });
  
  const instance = getCurrentInstance();
  const emitOpenLoginModal = () => {
    instance.emit('openLoginModal');
  };
  
  const weekDays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo'];
  
  // Mock data
  const volunteerSchedule = ref([
    { day: 'Segunda', time: '09:00 - 10:00', instrument: 'Violão Clássico (doado)', instrumentId: 'vol-violao1', booked: true },
    { day: 'Segunda', time: '10:00 - 11:00', instrument: 'Violão Clássico (doado)', instrumentId: 'vol-violao1', booked: false },
    { day: 'Quarta', time: '14:00 - 15:00', instrument: 'Flauta Doce (Prof. Silva)', instrumentId: 'vol-flauta1', booked: false },
  ]);
  
  const upcomingBookings = ref([
    { student: 'Maria Santos', instrument: 'Violão Clássico (doado)', date: '21/05/2025', time: '09:00 - 10:00' },
    { student: 'Pedro Oliveira', instrument: 'Ukulele (Voluntário)', date: '22/05/2025', time: '15:00 - 16:00' } // Exemplo
  ]);
  
  // Para o select de instrumentos que o voluntário gerencia
  const managedInstrumentsForSelect = ref([
      { id: 'vol-violao1', name: 'Violão Clássico (doado)', icon: GuitarIcon },
      { id: 'vol-flauta1', name: 'Flauta Doce (Prof. Silva)', icon: MusicIcon }
  ]);
  </script>