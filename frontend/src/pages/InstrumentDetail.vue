<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const isLoading = ref(true)
const instrument = ref(null)
const isReserved = ref(false) // Estado da reserva

onMounted(async () => {
  try {
    const response = await fetch('/data/instruments.json')
    const instruments = await response.json()

    // Busca o instrumento pelo ID da URL
    const instrumentId = route.params.id
    instrument.value = instruments.find(i => i.id === instrumentId)

    if (!instrument.value) {
      console.warn(`Instrument with ID ${instrumentId} not found.`)
      router.push('/instrument-wall')
      return
    }

  } catch (error) {
    console.error('Error loading instrument:', error)
  } finally {
    setTimeout(() => {
      isLoading.value = false
    }, 1000)
  }
})

// Função para reservar o instrumento
const reserveInstrument = () => {
  if (instrument.value.status !== "Available") return
  isReserved.value = true
  instrument.value.status = "Reserved"
}
</script>

<template>
  <div class="container">
    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading instrument details...</p>
    </div>

    <div v-else-if="instrument">
      <img :src="instrument.image" alt="Instrument Image" class="instrument-image" />
      <h1>{{ instrument.name }}</h1>
      <p class="description">{{ instrument.description }}</p>
      <p class="location">📍 Located at: <strong>{{ instrument.location }}</strong></p>
      <span class="status" :class="{ available: instrument.status === 'Available', unavailable: instrument.status !== 'Available' }">
        {{ isReserved ? 'Reserved' : instrument.status }}
      </span>

      <!-- Botão de reserva -->
      <button 
        v-if="instrument.status === 'Available' && !isReserved" 
        class="reserve-button"
        @click="reserveInstrument"
      >
        🎸 Reserve This Instrument
      </button>

      <p v-if="isReserved" class="reserved-message">✅ You have successfully reserved this instrument!</p>

      <!-- Botão para voltar -->
      <router-link to="/instrument-wall" class="back-button">
        <button>← Back to Instrument Wall</button>
      </router-link>
    </div>

    <div v-else class="error-container">
      <h1>Instrument not found</h1>
      <router-link to="/instrument-wall">
        <button>Back to Instrument Wall</button>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.instrument-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  border-radius: 8px;
  margin-bottom: 20px;
}

h1 {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 10px;
}

.description {
  font-size: 1.2rem;
  color: #555;
  text-align: center;
}

.location {
  text-align: center;
  font-size: 1.1rem;
  color: #007bff;
  margin-top: 10px;
}

.status {
  display: block;
  text-align: center;
  font-size: 1.1rem;
  font-weight: bold;
  margin-top: 10px;
  padding: 10px;
  border-radius: 5px;
}

.available {
  background: #28a745;
  color: white;
}

.unavailable {
  background: #dc3545;
  color: white;
}

/* Botão de reserva */
.reserve-button {
  display: block;
  margin: 20px auto;
  padding: 12px 20px;
  font-size: 1.1rem;
  border: none;
  border-radius: 25px;
  background: #ff9800;
  color: white;
  cursor: pointer;
  transition: background 0.2s ease-in-out;
  box-shadow: 0px 4px 8px rgba(255, 152, 0, 0.4);
}

.reserve-button:hover {
  background: #e68900;
  transform: scale(1.05);
  box-shadow: 0px 6px 12px rgba(255, 152, 0, 0.6);
}

.reserve-button:active {
  transform: scale(0.95);
}

/* Mensagem de reserva confirmada */
.reserved-message {
  text-align: center;
  font-size: 1.2rem;
  color: #28a745;
  font-weight: bold;
  margin-top: 10px;
}

/* Botão para voltar */
.back-button {
  display: flex;
  justify-content: center;
  margin-top: 30px;
  text-decoration: none;
}

.back-button button {
  background: #007bff;
  color: white;
  padding: 12px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease-in-out;
  box-shadow: 0px 4px 8px rgba(0, 123, 255, 0.3);
  display: flex;
  align-items: center;
  gap: 10px;
}

.back-button button:hover {
  background: #0056b3;
  transform: scale(1.05);
  box-shadow: 0px 6px 12px rgba(0, 123, 255, 0.5);
}

.back-button button:active {
  transform: scale(0.95);
}

/* Loading */
.loading-container {
  text-align: center;
  margin-top: 50px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(0, 123, 255, 0.3);
  border-top-color: #007bff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-container {
  text-align: center;
  color: red;
  margin-top: 50px;
}
</style>
