<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const course = ref(null)
const lessons = ref([])

onMounted(async () => {
  try {
    const response = await fetch('/data/learning_paths.json')
    const learningPaths = await response.json()
    course.value = learningPaths.find(c => c.id === route.params.id)

    if (!course.value) {
      console.warn('Course not found')
      router.push('/learning')
      return
    }

    const lessonsResponse = await fetch('/data/lessons.json')
    const allLessons = await lessonsResponse.json()
    lessons.value = allLessons.filter(l => l.learning_path_id === course.value.id)
  } catch (error) {
    console.error('Error loading course:', error)
  }
})
</script>

<template>
  <div class="container">
    <h1>{{ course?.name }}</h1>
    <p>{{ course?.description }}</p>

    <h2>Lessons:</h2>
    <ul>
      <li v-for="lesson in lessons" :key="lesson.id">
        <button @click="router.push(`/lesson/${lesson.id}`)">
          📖 {{ lesson.title }}
        </button>
      </li>
    </ul>

    <router-link to="/learning"><button>⬅ Back to Courses</button></router-link>
  </div>
</template>


<style scoped>
.container {
  max-width: 700px;
  margin: auto;
  padding: 20px;
}

h1, h2 {
  text-align: center;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  margin: 10px 0;
}

button {
  background: #007bff;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
}

button:hover {
  background: #0056b3;
}
</style>
