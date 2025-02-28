<script setup>
import { ref, onMounted, computed } from 'vue'

const learningPaths = ref([])
const searchQuery = ref("") // Filtro por nome
const selectedInstrument = ref("") // Filtro por tipo de instrumento
const instrumentTypes = ref([]) // Lista de tipos de instrumentos disponíveis

onMounted(async () => {
  try {
    const response = await fetch('/data/learning_paths.json')
    learningPaths.value = await response.json()

    // Carregar tipos de instrumentos (simulado)
    const instrumentsResponse = await fetch('/data/instrument_types.json')
    instrumentTypes.value = await instrumentsResponse.json()
  } catch (error) {
    console.error('Error loading courses:', error)
  }
})

// Computed para filtrar cursos dinamicamente
const filteredLearningPaths = computed(() => {
  return learningPaths.value.filter(course => {
    const matchesName = course.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesInstrument = selectedInstrument.value
      ? course.instrument_type_id === selectedInstrument.value
      : true
    return matchesName && matchesInstrument
  })
})
</script>

<template>
  <div class="container">
    <h1>🎵 Available Courses</h1>

    <!-- Filtros -->
    <div class="filters">
      <input type="text" v-model="searchQuery" placeholder="Search by course name..." />

      <select v-model="selectedInstrument">
        <option value="">All Instruments</option>
        <option v-for="instrument in instrumentTypes" :key="instrument.id" :value="instrument.id">
          {{ instrument.name }}
        </option>
      </select>
    </div>

    <div v-if="filteredLearningPaths.length === 0">
      <p>No courses found.</p>
    </div>

    <div v-else class="courses-list">
      <div v-for="course in filteredLearningPaths" :key="course.id" class="course-card">
        <h2>{{ course.name }}</h2>
        <p>{{ course.description }}</p>
        <button @click="$router.push(`/learning-path/${course.id}`)">📚 View Course</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

h1 {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 20px;
}

/* Filtros */
.filters {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.filters input,
.filters select {
  padding: 10px;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #ccc;
  width: 48%;
}

/* Lista de cursos */
.courses-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.course-card {
  background: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

button {
  background: #007bff;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}
</style>
