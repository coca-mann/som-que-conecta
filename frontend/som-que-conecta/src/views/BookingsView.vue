<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 mb-2">
              Agendamentos
            </h1>
            <p class="text-gray-600">
              Gerencie os agendamentos dos seus instrumentos
            </p>
          </div>
            
          <div class="mt-4 sm:mt-0 flex items-center space-x-3">
            <select 
              v-model="selectedStatus" 
              class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            >
              <option value="">
                Todos os Status
              </option>
              <option value="PENDING">
                Pendente
              </option>
              <option value="APPROVED">
                Aprovado
              </option>
              <option value="REJECTED">
                Rejeitado
              </option>
            </select>
              
            <div class="flex bg-gray-100 rounded-lg p-1">
              <button
                :class="[
                  'px-3 py-1 text-sm font-medium rounded-md transition-all duration-200',
                  currentView === 'calendar' 
                    ? 'bg-white text-red-600 shadow-sm' 
                    : 'text-gray-500 hover:text-gray-700'
                ]"
                @click="currentView = 'calendar'"
              >
                <Calendar class="h-4 w-4 inline mr-1" />
                Calendário
              </button>
              <button
                :class="[
                  'px-3 py-1 text-sm font-medium rounded-md transition-all duration-200',
                  currentView === 'list' 
                    ? 'bg-white text-red-600 shadow-sm' 
                    : 'text-gray-500 hover:text-gray-700'
                ]"
                @click="currentView = 'list'"
              >
                <List class="h-4 w-4 inline mr-1" />
                Lista
              </button>
            </div>
          </div>
        </div>
      </div>
 
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center">
                <Clock class="h-5 w-5 text-yellow-600" />
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">
                Pendentes
              </p>
              <p class="text-2xl font-semibold text-gray-900">
                {{ stats.pending }}
              </p>
            </div>
          </div>
        </div>
          
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                <CheckCircle class="h-5 w-5 text-green-600" />
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">
                Confirmados
              </p>
              <p class="text-2xl font-semibold text-gray-900">
                {{ stats.confirmed }}
              </p>
            </div>
          </div>
        </div>
          
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                <XCircle class="h-5 w-5 text-red-600" />
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">
                Rejeitados
              </p>
              <p class="text-2xl font-semibold text-gray-900">
                {{ stats.rejected }}
              </p>
            </div>
          </div>
        </div>
          
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div class="w-8 h-8 bg-red-100 rounded-lg flex items-center justify-center">
                <TrendingUp class="h-5 w-5 text-red-600" />
              </div>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-500">
                Este Mês
              </p>
              <p class="text-2xl font-semibold text-gray-900">
                {{ stats.thisMonth }}
              </p>
            </div>
          </div>
        </div>
      </div>
 
      <div
        v-if="currentView === 'calendar'"
        class="bg-white rounded-lg shadow-sm p-6"
      >
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold text-gray-900">
            {{ formatMonthYear(currentDate) }}
          </h2>
          <div class="flex items-center space-x-2">
            <button
              class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors duration-200"
              @click="previousMonth"
            >
              <ChevronLeft class="h-5 w-5" />
            </button>
            <button
              class="px-3 py-1 text-sm bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors duration-200"
              @click="goToToday"
            >
              Hoje
            </button>
            <button
              class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors duration-200"
              @click="nextMonth"
            >
              <ChevronRight class="h-5 w-5" />
            </button>
          </div>
        </div>
 
        <div class="grid grid-cols-7 gap-px bg-gray-200 rounded-lg overflow-hidden">
          <div
            v-for="day in dayHeaders"
            :key="day"
            class="bg-gray-50 p-3 text-center text-sm font-medium text-gray-500"
          >
            {{ day }}
          </div>
 
          <div
            v-for="day in calendarDays"
            :key="`${day.date}-${day.isCurrentMonth}`"
            :class="[
              'bg-white p-2 min-h-[120px] relative',
              !day.isCurrentMonth ? 'bg-gray-50 text-gray-400' : '',
              isToday(day.date) ? 'bg-red-50' : ''
            ]"
          >
            <div class="flex items-center justify-between mb-2">
              <span
                :class="[
                  'text-sm font-medium',
                  isToday(day.date) ? 'text-red-600' : day.isCurrentMonth ? 'text-gray-900' : 'text-gray-400'
                ]"
              >
                {{ day.date.getDate() }}
              </span>
              <div
                v-if="getBookingsForDay(day.date).length > 0"
                class="flex space-x-1"
              >
                <div class="w-2 h-2 bg-red-500 rounded-full" />
              </div>
            </div>
 
            <div class="space-y-1">
              <div
                v-for="booking in getBookingsForDay(day.date).slice(0, 2)"
                :key="booking.id"
                :class="[
                  'text-xs p-1 rounded cursor-pointer transition-colors duration-200',
                  getStatusColor(booking.status)
                ]"
                @click="openBookingModal(booking)"
              >
                <div class="font-medium truncate">
                  {{ booking.instrument.name }}
                </div>
                <div class="truncate">
                  {{ formatTime(booking.startTime) }}
                </div>
              </div>
                
              <div
                v-if="getBookingsForDay(day.date).length > 2"
                class="text-xs text-gray-500 cursor-pointer hover:text-gray-700"
                @click="showDayBookings(day.date)"
              >
                +{{ getBookingsForDay(day.date).length - 2 }} mais
              </div>
            </div>
          </div>
        </div>
      </div>
 
      <div
        v-else
        class="bg-white rounded-lg shadow-sm overflow-hidden"
      >
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-xl font-semibold text-gray-900">
            Lista de Agendamentos
          </h2>
        </div>
 
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Instrumento
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Cliente
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Data e Hora
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Duração
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr
                v-for="booking in filteredBookings"
                :key="booking.id"
                class="hover:bg-gray-50 transition-colors duration-200"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <img
                      :src="booking.instrument.main_image"
                      :alt="booking.instrument.name"
                      class="h-10 w-10 rounded-lg object-cover"
                    >
                    <div class="ml-4">
                      <div class="text-sm font-medium text-gray-900">
                        {{ booking.instrument.name }}
                      </div>
                      <div class="text-sm text-gray-500">
                        {{ booking.instrument.brand }}
                      </div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <img
                      :src="booking.client.profile_picture"
                      :alt="booking.client.name"
                      class="h-8 w-8 rounded-full"
                    >
                    <div class="ml-3">
                      <div class="text-sm font-medium text-gray-900">
                        {{ booking.client.name }}
                      </div>
                      <div class="text-sm text-gray-500">
                        {{ booking.client.email }}
                      </div>
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  <div>{{ formatDate(booking.startTime) }}</div>
                  <div class="text-gray-500">
                    {{ formatTime(booking.startTime) }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                  {{ calculateDuration(booking.startTime, booking.endTime) }}h
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      getStatusBadgeColor(booking.status)
                    ]"
                  >
                    {{ getStatusLabel(booking.status) }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                  <button
                    class="text-red-600 hover:text-red-900 transition-colors duration-200"
                    @click="openBookingModal(booking)"
                  >
                    Ver Detalhes
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
 
        <div
          v-if="filteredBookings.length === 0"
          class="text-center py-12"
        >
          <CalendarDays class="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <h3 class="text-lg font-medium text-gray-900 mb-2">
            Nenhum agendamento encontrado
          </h3>
          <p class="text-gray-600">
            {{ selectedStatus ? 'Não há agendamentos com este status.' : 'Você ainda não possui agendamentos.' }}
          </p>
        </div>
      </div>
    </div>
 
    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="selectedBooking"
        class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      >
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
          <div class="flex items-center justify-between p-6 border-b border-gray-200">
            <h3 class="text-xl font-semibold text-gray-900">
              Detalhes do Agendamento
            </h3>
            <button
              class="text-gray-400 hover:text-red-600 transition-colors duration-200"
              @click="closeBookingModal"
            >
              <X class="h-6 w-6" />
            </button>
          </div>
 
          <div class="p-6 space-y-6">
            <div class="grid md:grid-cols-2 gap-6">
              <div>
                <h4 class="text-sm font-medium text-gray-500 mb-3">
                  Instrumento
                </h4>
                <div class="flex items-center space-x-3">
                  <img
                    :src="selectedBooking.instrument.main_image"
                    :alt="selectedBooking.instrument.name"
                    class="h-16 w-16 rounded-lg object-cover"
                  >
                  <div>
                    <div class="font-medium text-gray-900">
                      {{ selectedBooking.instrument.name }}
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ selectedBooking.instrument.brand }}
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ selectedBooking.instrument.type }}
                    </div>
                  </div>
                </div>
              </div>
 
              <div>
                <h4 class="text-sm font-medium text-gray-500 mb-3">
                  Cliente
                </h4>
                <div class="flex items-center space-x-3">
                  <img
                    :src="selectedBooking.client.profile_picture"
                    :alt="selectedBooking.client.name"
                    class="h-16 w-16 rounded-full"
                  >
                  <div>
                    <div class="font-medium text-gray-900">
                      {{ selectedBooking.client.name }}
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ selectedBooking.client.email }}
                    </div>
                    <div class="text-sm text-gray-500">
                      {{ selectedBooking.client.phone }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
 
            <div class="grid md:grid-cols-3 gap-4">
              <div>
                <h4 class="text-sm font-medium text-gray-500 mb-2">
                  Data
                </h4>
                <div class="flex items-center space-x-2">
                  <Calendar class="h-4 w-4 text-gray-400" />
                  <span class="text-gray-900">{{ formatDate(selectedBooking.startTime) }}</span>
                </div>
              </div>
              <div>
                <h4 class="text-sm font-medium text-gray-500 mb-2">
                  Horário
                </h4>
                <div class="flex items-center space-x-2">
                  <Clock class="h-4 w-4 text-gray-400" />
                  <span class="text-gray-900">
                    {{ formatTime(selectedBooking.startTime) }} - {{ formatTime(selectedBooking.endTime) }}
                  </span>
                </div>
              </div>
              <div>
                <h4 class="text-sm font-medium text-gray-500 mb-2">
                  Duração
                </h4>
                <div class="flex items-center space-x-2">
                  <Timer class="h-4 w-4 text-gray-400" />
                  <span class="text-gray-900">{{ calculateDuration(selectedBooking.startTime, selectedBooking.endTime) }}h</span>
                </div>
              </div>
            </div>
 
            <div>
              <h4 class="text-sm font-medium text-gray-500 mb-2">
                Status
              </h4>
              <span
                :class="[
                  'inline-flex items-center px-3 py-1 rounded-full text-sm font-medium',
                  getStatusBadgeColor(selectedBooking.status)
                ]"
              >
                {{ getStatusLabel(selectedBooking.status) }}
              </span>
            </div>
 
            <div v-if="selectedBooking.notes">
              <h4 class="text-sm font-medium text-gray-500 mb-2">
                Observações
              </h4>
              <p class="text-gray-900 bg-gray-50 p-3 rounded-lg">
                {{ selectedBooking.notes }}
              </p>
            </div>
 
            <div v-if="selectedBooking.status === 'rejected' && selectedBooking.rejectionReason">
              <h4 class="text-sm font-medium text-gray-500 mb-2">
                Motivo da Rejeição
              </h4>
              <p class="text-red-700 bg-red-50 p-3 rounded-lg border border-red-200">
                {{ selectedBooking.rejectionReason }}
              </p>
            </div>
 
            <div
              v-if="showRejectionForm"
              class="border-t border-gray-200 pt-6"
            >
              <h4 class="text-sm font-medium text-gray-500 mb-3">
                Motivo da Rejeição
              </h4>
              <textarea
                v-model="rejectionReason"
                rows="3"
                placeholder="Explique o motivo da rejeição..."
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent resize-none"
              />
            </div>
          </div>
 
          <div class="flex items-center justify-end space-x-3 p-6 border-t border-gray-200 bg-gray-50">
            <button
              class="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors duration-200"
              @click="closeBookingModal"
            >
              Fechar
            </button>
              
            <div
              v-if="selectedBooking.status === 'PENDING'"
              class="flex space-x-3"
            >
              <button
                :disabled="isProcessing"
                class="px-4 py-2 text-white bg-red-600 rounded-lg hover:bg-red-700 disabled:opacity-50 transition-colors duration-200 flex items-center space-x-2"
                @click="showRejectionForm ? rejectBooking() : (showRejectionForm = true)"
              >
                <XCircle class="h-4 w-4" />
                <span>{{ showRejectionForm ? 'Confirmar Rejeição' : 'Rejeitar' }}</span>
              </button>
                
              <button
                v-if="!showRejectionForm"
                :disabled="isProcessing"
                class="px-4 py-2 text-white bg-green-600 rounded-lg hover:bg-green-700 disabled:opacity-50 transition-colors duration-200 flex items-center space-x-2"
                @click="acceptBooking"
              >
                <CheckCircle class="h-4 w-4" />
                <span>Aceitar</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>
  
  <script setup>
import { ref, computed, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth.store';
import instrumentService from '@/services/instrumentService';
import {
  Calendar, List, Clock, CheckCircle, XCircle, TrendingUp,
  ChevronLeft, ChevronRight, X, Timer, CalendarDays, MapPin
} from 'lucide-vue-next';
import { useHead } from '@vueuse/head';

useHead({
  title: 'Gerenciar Agendamentos | Som que Conecta',
  meta: [
    { name: 'description', content: 'Gerencie os agendamentos dos seus instrumentos musicais.' },
  ]
})

// --- ESTADO PRINCIPAL ---
const bookings = ref([]);
const isLoading = ref(true);
const error = ref(null);
const currentView = ref('calendar');
const selectedStatus = ref('');
const currentDate = ref(new Date());
const selectedBooking = ref(null);
const showRejectionForm = ref(false);
const rejectionReason = ref('');
const isProcessing = ref(false);
const dayHeaders = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];

// --- LÓGICA DE DADOS ---
const fetchBookings = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    const response = await instrumentService.getBookings();
    bookings.value = response.data.map(booking => ({
      ...booking,
      startTime: new Date(`${booking.reservation_date}T${booking.reservation_starttime}`),
      endTime: new Date(`${booking.reservation_date}T${booking.reservation_endtime}`),
    }));
  } catch (err) {
    console.error("Erro ao buscar agendamentos:", err);
    error.value = "Não foi possível carregar os agendamentos.";
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchBookings();
});

// --- PROPRIEDADES COMPUTADAS (Corrigidas) ---
const stats = computed(() => ({
  pending: bookings.value.filter(b => b.status === 'PENDING').length,
  confirmed: bookings.value.filter(b => b.status === 'APPROVED').length,
  rejected: bookings.value.filter(b => b.status === 'REJECTED').length,
  thisMonth: bookings.value.filter(b => new Date(b.startTime).getMonth() === new Date().getMonth()).length
}));

const filteredBookings = computed(() => {
  if (!selectedStatus.value) return bookings.value;
  return bookings.value.filter(booking => booking.status === selectedStatus.value);
});

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth();
  const firstDay = new Date(year, month, 1);
  const startDate = new Date(firstDay);
  startDate.setDate(startDate.getDate() - firstDay.getDay());
  const days = [];
  const current = new Date(startDate);
  for (let i = 0; i < 42; i++) {
    days.push({ date: new Date(current), isCurrentMonth: current.getMonth() === month });
    current.setDate(current.getDate() + 1);
  }
  return days;
});

// --- MÉTODOS DE FORMATAÇÃO E UI (Adicionados) ---
const formatMonthYear = date => new Intl.DateTimeFormat('pt-BR', { month: 'long', year: 'numeric' }).format(date);
const formatDate = date => new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' }).format(date);
const formatTime = date => new Intl.DateTimeFormat('pt-BR', { hour: '2-digit', minute: '2-digit' }).format(date);
const isToday = date => new Date().toDateString() === date.toDateString();
const getBookingsForDay = (date) => filteredBookings.value.filter(b => new Date(b.startTime).toDateString() === date.toDateString());

const calculateDuration = (startTime, endTime) => {
  const start = new Date(startTime);
  const end = new Date(endTime);
  const diffInHours = (end - start) / (1000 * 60 * 60);
  return diffInHours.toFixed(1);
};

const getStatusColor = (status) => {
  const colors = {
    PENDING: 'bg-yellow-100 text-yellow-800 hover:bg-yellow-200',
    APPROVED: 'bg-green-100 text-green-800 hover:bg-green-200',
    REJECTED: 'bg-red-100 text-red-800 hover:bg-red-200',
    COMPLETED: 'bg-blue-100 text-blue-800 hover:bg-blue-200'
  };
  return colors[status] || 'bg-gray-100 text-gray-800 hover:bg-gray-200';
};

const getStatusBadgeColor = (status) => {
  const colors = {
    PENDING: 'bg-yellow-100 text-yellow-800',
    APPROVED: 'bg-green-100 text-green-800',
    REJECTED: 'bg-red-100 text-red-800',
    COMPLETED: 'bg-blue-100 text-blue-800'
  };
  return colors[status] || 'bg-gray-100 text-gray-800';
};

const getStatusLabel = (status) => {
  const labels = {
    PENDING: 'Pendente',
    APPROVED: 'Aprovado',
    REJECTED: 'Rejeitado',
    COMPLETED: 'Concluído'
  };
  return labels[status] || status;
};

// --- MÉTODOS DE AÇÃO ---
const previousMonth = () => { currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1); };
const nextMonth = () => { currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1); };
const goToToday = () => { currentDate.value = new Date(); };

const openBookingModal = (booking) => {
  selectedBooking.value = booking;
  showRejectionForm.value = false;
  rejectionReason.value = '';
};

const closeBookingModal = () => { selectedBooking.value = null; };

const updateLocalBookingStatus = (bookingId, newStatus, reason = null) => {
  const index = bookings.value.findIndex(b => b.id === bookingId);
  if (index !== -1) {
    bookings.value[index].status = newStatus;
    if (reason) bookings.value[index].reservation_refusal_reason = reason;
  }
};

const acceptBooking = async () => {
  if (!selectedBooking.value) return;
  isProcessing.value = true;
  try {
    await instrumentService.updateBookingStatus(selectedBooking.value.id, { status: 'APPROVED' });
    updateLocalBookingStatus(selectedBooking.value.id, 'APPROVED');
    closeBookingModal();
  } catch (error) {
    alert("Falha ao aceitar o agendamento.");
  } finally {
    isProcessing.value = false;
  }
};

const rejectBooking = async () => {
  if (!selectedBooking.value || !rejectionReason.value.trim()) {
    alert('Por favor, informe o motivo da rejeição.');
    return;
  }
  isProcessing.value = true;
  const payload = {
    status: 'REJECTED',
    reservation_refusal_reason: rejectionReason.value.trim()
  };
  try {
    await instrumentService.updateBookingStatus(selectedBooking.value.id, payload);
    updateLocalBookingStatus(selectedBooking.value.id, 'REJECTED', payload.reservation_refusal_reason);
    closeBookingModal();
  } catch (error) {
    alert("Falha ao rejeitar o agendamento.");
  } finally {
    isProcessing.value = false;
  }
};
  </script>
  
  const showDayBookings = (date) => { console.log('Show bookings for:', date); };
  
  <style scoped>
  /* Custom scrollbar */
  .overflow-y-auto::-webkit-scrollbar {
    width: 6px;
  }
  
  .overflow-y-auto::-webkit-scrollbar-track {
    background: #f1f5f9;
  }
  
  .overflow-y-auto::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 3px;
  }
  
  .overflow-y-auto::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
  }
  </style>
  