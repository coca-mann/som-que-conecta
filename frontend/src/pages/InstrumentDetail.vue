<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { format, isSameDay, parseISO } from 'date-fns'

const route = useRoute()
const router = useRouter()
const isLoading = ref(true)
const instrument = ref(null)
const availability = ref([]) // Disponibilidade do instrumento
const today = new Date()

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

    // Carregar disponibilidade simulada da API (mock)
    const availabilityResponse = await fetch('/data/instrument_availability_mock.json')
    const allAvailability = await availabilityResponse.json()
    availability.value = allAvailability
      .filter(a => a.instrument_id === instrumentId)
      .filter(a => isSameDay(parseISO(a.available_from), today))

  } catch (error) {
    console.error('Error loading instrument:', error)
  } finally {
    setTimeout(() => {
      isLoading.value = false
    }, 1000)
  }
})
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

      <div class="instrument-details">
        <p><strong>Descrição:</strong> {{ instrument.description }}</p>
        <p><strong>Tipo:</strong> {{ instrument.type }}</p>
        <p><strong>Marca:</strong> {{ instrument.brand }}</p>
        <p><strong>Cor:</strong> {{ instrument.color }}</p>
        <p><strong>Localização:</strong> 📍 {{ instrument.location }}</p>
        <p><strong>Registrado por:</strong> {{ instrument.owner }}</p>
        <p><strong>Data de Cadastro:</strong> {{ new Date(instrument.created_at).toLocaleDateString() }}</p>
      </div>

      <span class="status" :class="{ available: instrument.status === 'Available', unavailable: instrument.status !== 'Available' }">
        {{ instrument.status }}
      </span>

      <!-- Disponibilidade de Hoje -->
      <div class="availability-section">
        <h2>📅 Disponibilidade para Hoje</h2>
        <p v-if="availability.length === 0">Nenhuma disponibilidade para hoje.</p>

        <ul v-else>
          <li v-for="slot in availability" :key="slot.id">
            {{ format(parseISO(slot.available_from), 'HH:mm') }} - {{ format(parseISO(slot.available_to), 'HH:mm') }}
            <span class="badge">Disponível</span>
          </li>
        </ul>
      </div>

      <!-- Botão para voltar -->
      <router-link to="/instrument-wall" class="back-button">
        <button>← Voltar para o Mural</button>
      </router-link>
    </div>

    <div v-else class="error-container">
      <h1>Instrumento não encontrado</h1>
      <router-link to="/instrument-wall">
        <button>Voltar para o Mural</button>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 700px;
  margin: auto;
  padding: 20px;
}

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

.instrument-details {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 15px;
}

.status {
  display: block;
  text-align: center;
  font-size: 1.2rem;
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

/* Seção de Disponibilidade */
.availability-section {
  margin-top: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.availability-section h2 {
  font-size: 1.4rem;
  margin-bottom: 10px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 10px;
  margin: 5px 0;
  border-radius: 5px;
  font-size: 1.1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #d4edda;
  color: #155724;
}

.badge {
  font-size: 0.9rem;
  padding: 5px 10px;
  border-radius: 5px;
  background: #28a745;
  color: white;
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
}

.back-button button:hover {
  background: #0056b3;
}

.error-container {
  text-align: center;
  color: red;
  margin-top: 50px;
}
</style>
