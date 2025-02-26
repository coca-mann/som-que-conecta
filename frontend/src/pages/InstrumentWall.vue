<script setup>
import { ref, onMounted, computed } from 'vue'
import InstrumentCard from '../components/InstrumentCard.vue'

const instruments = ref([])
const searchQuery = ref('')
const filterStatus = ref('All')

onMounted(async () => {
  try {
    const response = await fetch('/data/instruments.json')
    instruments.value = await response.json()
  } catch (error) {
    console.error('Failed to load instruments:', error)
  }
})

// Filtra os instrumentos pelo nome e status
const filteredInstruments = computed(() => {
  return instruments.value.filter(instrument => {
    const matchesSearch = instrument.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesStatus = filterStatus.value === 'All' || instrument.status === filterStatus.value
    return matchesSearch && matchesStatus
  })
})
</script>

<template>
  <div class="container">
    <h1>Instrument Wall 🎸</h1>
    <p>Find available musical instruments to use.</p>

    <!-- Filtros -->
    <div class="filters">
      <input v-model="searchQuery" type="text" placeholder="Search instruments..." />
      <select v-model="filterStatus">
        <option value="All">All</option>
        <option value="Available">Available</option>
        <option value="Unavailable">Unavailable</option>
      </select>
    </div>

    <!-- Exibição dos instrumentos -->
    <div class="instruments">
      <InstrumentCard v-for="instrument in filteredInstruments" :key="instrument.id" :instrument="instrument" />
    </div>

    <!-- Caso não encontre nenhum instrumento -->
    <div v-if="filteredInstruments.length === 0" class="no-results">
      <p>No instruments found.</p>
    </div>
  </div>
</template>

<style scoped>
/* Filtros */
.filters {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  gap: 10px;
}

.filters input, .filters select {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
}

/* Grid de instrumentos */
.instruments {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

/* Mensagem quando nenhum instrumento for encontrado */
.no-results {
  text-align: center;
  font-size: 1.2rem;
  color: #777;
  font-style: italic;
  margin-top: 20px;
}

/* Responsividade */
@media (max-width: 600px) {
  .filters {
    flex-direction: column;
  }
}
</style>
