<template>
    <div v-if="loading" class="text-center py-10">Carregando agenda do instrumento...</div>
    <div v-else-if="!selectedInstrument" class="text-center py-10 text-red-500">Instrumento não encontrado ou indisponível.</div>
    <div v-else class="space-y-6">
      <div class="flex items-center mb-6">
        <router-link 
          to="/instrumentos"
          class="mr-4 p-2 rounded-full hover:bg-gray-100"
        >
          <ArrowLeftIcon class="h-5 w-5 text-gray-700" />
        </router-link>
        <h1 class="text-3xl font-bold text-emerald-800">Disponibilidade: {{ selectedInstrument.name }}</h1>
      </div>
      
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="p-6">
          <div class="flex items-center mb-6">
            <div class="bg-emerald-100 p-3 rounded-md mr-4">
              <component :is="selectedInstrument.icon" class="h-10 w-10 text-emerald-600" />
            </div>
            <div>
              <h2 class="text-xl font-semibold">{{ selectedInstrument.name }}</h2>
              <p class="text-gray-500">{{ selectedInstrument.description }}</p>
              <span class="inline-block mt-1 px-2 py-1 bg-emerald-100 text-emerald-800 rounded-full text-xs">
                Disponibilizado por: {{ selectedInstrument.source }}
              </span>
            </div>
          </div>
          
          <div class="mb-6">
            <h3 class="text-lg font-semibold mb-3">Selecione um Dia e Horário</h3>
            <div class="grid grid-cols-7 gap-2 mb-4 text-center">
              <div v-for="day in weekDays" :key="day" class="font-medium text-sm text-gray-600">{{ day }}</div>
              <div 
                v-for="dateSlot in calendarDays" 
                :key="dateSlot.fullDate"
                class="aspect-square border rounded-md flex items-center justify-center cursor-pointer hover:bg-gray-50"
                :class="{
                  'bg-emerald-500 text-white hover:bg-emerald-600': selectedDay === dateSlot.date && dateSlot.hasSlots,
                  'bg-emerald-100 border-emerald-300': selectedDay === dateSlot.date && dateSlot.hasSlots,
                  'text-gray-400 cursor-not-allowed': !dateSlot.hasSlots && !dateSlot.isToday,
                  'bg-gray-100': !dateSlot.hasSlots,
                  'font-bold text-emerald-700 ring-2 ring-emerald-300': dateSlot.isToday
                }"
                @click="dateSlot.hasSlots ? selectDay(dateSlot.date) : null"
              >
                {{ dateSlot.date }}
              </div>
            </div>
            
            <div v-if="selectedDay !== null" class="border rounded-md p-4">
              <h4 class="font-medium mb-3">Horários disponíveis para {{ formattedSelectedDate }}</h4>
              <div v-if="currentAvailableTimeSlots.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
                <button 
                  v-for="(slot, index) in currentAvailableTimeSlots" 
                  :key="index"
                  class="py-2 px-3 border rounded-md text-center text-sm"
                  :class="{
                      'bg-emerald-600 text-white border-emerald-700': selectedTimeSlot === slot.time,
                      'hover:bg-emerald-50': selectedTimeSlot !== slot.time && slot.available,
                      'bg-gray-200 text-gray-400 cursor-not-allowed': !slot.available
                  }"
                  @click="slot.available ? selectedTimeSlot = slot.time : null"
                  :disabled="!slot.available"
                >
                  {{ slot.time }} <span v-if="!slot.available">(Indisp.)</span>
                </button>
              </div>
               <div v-else class="text-gray-500">Nenhum horário disponível para este dia.</div>
              
              <div class="mt-4 flex justify-end">
                <button 
                  :disabled="selectedTimeSlot === null"
                  :class="{
                      'bg-emerald-600 hover:bg-emerald-500 text-white': selectedTimeSlot !== null, 
                      'bg-gray-300 cursor-not-allowed text-gray-500': selectedTimeSlot === null
                  }"
                  class="px-4 py-2 rounded-md transition-colors"
                  @click="bookSlot"
                >
                  Reservar Horário
                </button>
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
      Guitar as GuitarIcon, 
      Piano as PianoIcon, 
      Drum as DrumIcon, 
      Mic as MicIcon,
      Music as MusicIcon // Genérico
  } from 'lucide-vue-next';
  
  const props = defineProps({
    instrumentId: String, // Recebido do router
    isLoggedIn: Boolean
  });
  
  const route = useRoute();
  const loading = ref(true);
  const selectedInstrument = ref(null);
  const selectedDay = ref(null); // Dia do mês
  const selectedTimeSlot = ref(null); // String do horário, ex: "09:00 - 10:00"
  
  // Mock de dados de instrumentos (deveria vir de um store ou API)
  const allInstrumentsData = ref([
    { id: 'violao1', name: 'Violão Clássico', description: 'Violão para iniciantes.', source: 'ONGs', icon: GuitarIcon, availability: { /* ... */ } },
    { id: 'piano1', name: 'Piano Digital', description: 'Piano digital com 88 teclas.', source: 'Professores', icon: PianoIcon, availability: { /* ... */ } },
    { id: 'flauta1', name: 'Flauta Doce', description: 'Flauta para iniciantes.', source: 'ONGs', icon: MusicIcon, availability: { /* ... */ } },
    { id: 'ukulele1', name: 'Ukulele', description: 'Ukulele soprano.', source: 'Professores', icon: GuitarIcon, availability: { /* ... */ } },
    { id: 'bateria1', name: 'Bateria Eletrônica', description: 'Bateria para prática.', source: 'Professores', icon: DrumIcon, availability: { /* ... */ } },
    { id: 'mic1', name: 'Microfone', description: 'Microfone dinâmico.', source: 'ONGs', icon: MicIcon, availability: { /* ... */ } }
  ]);
  
  // Mock de horários disponíveis (complexo para simular realisticamente sem um backend)
  const instrumentTimeSlots = ref({ // instrumentId: { 'YYYY-MM-DD': [{time: "HH:MM - HH:MM", available: true}, ...] }
      'violao1': {
          '2025-05-21': [{time: "09:00 - 10:00", available: true}, {time: "10:00 - 11:00", available: false}, {time: "14:00 - 15:00", available: true}],
          '2025-05-22': [{time: "10:00 - 11:00", available: true}, {time: "15:00 - 16:00", available: true}],
      },
      'piano1': {
          '2025-05-21': [{time: "11:00 - 12:00", available: true}],
      }
  });
  
  const weekDays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
  const calendarDays = ref([]); // Será preenchido com { date: DD, fullDate: 'YYYY-MM-DD', hasSlots: boolean, isToday: boolean }
  
  const generateCalendarDays = () => {
      const today = new Date();
      const currentMonth = today.getMonth();
      const currentYear = today.getFullYear();
      calendarDays.value = [];
      for (let i = 1; i <= 7; i++) { // Simular próximos 7 dias
          const day = new Date(currentYear, currentMonth, today.getDate() + i -1); // Começando de hoje
          const dayDate = day.getDate();
          const fullDateStr = `${day.getFullYear()}-${String(day.getMonth() + 1).padStart(2, '0')}-${String(dayDate).padStart(2, '0')}`;
          
          const slotsForDay = instrumentTimeSlots.value[props.instrumentId]?.[fullDateStr] || [];
          calendarDays.value.push({
              date: dayDate,
              fullDate: fullDateStr,
              hasSlots: slotsForDay.some(s => s.available),
              isToday: day.toDateString() === new Date().toDateString() // Marcar hoje
          });
      }
  };
  
  
  onMounted(() => {
    const id = props.instrumentId || route.params.instrumentId;
    setTimeout(() => { // Simula busca
      selectedInstrument.value = allInstrumentsData.value.find(i => i.id === id) || null;
      if (selectedInstrument.value) {
          generateCalendarDays();
      }
      loading.value = false;
    }, 300);
  });
  
  const currentAvailableTimeSlots = computed(() => {
      if (!selectedInstrument.value || selectedDay.value === null) return [];
      // Encontrar a data completa para o dia selecionado no mês atual
      const dayData = calendarDays.value.find(d => d.date === selectedDay.value);
      if (!dayData) return [];
  
      return instrumentTimeSlots.value[props.instrumentId]?.[dayData.fullDate] || [];
  });
  
  const formattedSelectedDate = computed(() => {
      if (selectedDay.value === null) return '';
      const dayData = calendarDays.value.find(d => d.date === selectedDay.value);
      if (!dayData) return '';
      const dateObj = new Date(dayData.fullDate + 'T00:00:00'); // Adiciona T00:00:00 para evitar problemas de fuso horário na formatação
      return dateObj.toLocaleDateString('pt-BR', { weekday: 'long', day: 'numeric', month: 'long' });
  });
  
  const selectDay = (day) => {
    selectedDay.value = day;
    selectedTimeSlot.value = null; // Reseta o horário ao mudar o dia
  };
  
  const bookSlot = () => {
    if (!selectedDay.value || !selectedTimeSlot.value || !props.isLoggedIn) {
      if(!props.isLoggedIn) alert('Você precisa estar logado para reservar.');
      else alert('Por favor, selecione um dia e um horário.');
      return;
    }
    // Lógica de reserva (ex: chamada API)
    alert(`Horário ${selectedTimeSlot.value} no dia ${formattedSelectedDate.value} para ${selectedInstrument.value.name} reservado com sucesso! (Simulação)`);
    // Marcar como indisponível (simulação)
      const dayData = calendarDays.value.find(d => d.date === selectedDay.value);
      if (dayData && instrumentTimeSlots.value[props.instrumentId]?.[dayData.fullDate]) {
          const slot = instrumentTimeSlots.value[props.instrumentId][dayData.fullDate].find(s => s.time === selectedTimeSlot.value);
          if (slot) slot.available = false;
      }
    selectedTimeSlot.value = null; // Limpa seleção
    generateCalendarDays(); // Regenera para refletir a mudança de disponibilidade (se hasSlots mudou)
  };
  </script>