<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const lesson = ref(null)
const lessons = ref([])
const completedLessons = ref(new Set())

// Função para carregar progresso salvo no localStorage
const loadProgress = () => {
  const savedProgress = JSON.parse(localStorage.getItem("completedLessons")) || [];
  completedLessons.value = new Set(savedProgress);
};

// Função para salvar progresso no localStorage
const saveProgress = () => {
  localStorage.setItem("completedLessons", JSON.stringify([...completedLessons.value]));
};

// Função para marcar lição como concluída
const markAsCompleted = () => {
  if (lesson.value) {
    completedLessons.value.add(lesson.value.id);
    saveProgress();
  }
};

// Verifica se a lição atual está concluída
const isLessonCompleted = computed(() => {
  return lesson.value ? completedLessons.value.has(lesson.value.id) : false;
});

const loadLesson = async () => {
  try {
    const response = await fetch('/data/lessons.json')
    const allLessons = await response.json()

    // Encontrar a lição atual
    lesson.value = allLessons.find(l => l.id === route.params.id)

    if (!lesson.value) {
      console.warn('Lesson not found')
      router.push('/learning')
      return
    }

    // Carregar todas as lições do curso atual
    lessons.value = allLessons.filter(l => l.learning_path_id === lesson.value.learning_path_id)
    
    // Carregar progresso salvo
    loadProgress();
  } catch (error) {
    console.error('Error loading lesson:', error)
  }
};

// Carregar os dados ao iniciar a página
onMounted(loadLesson)

// Atualizar os dados sempre que a rota mudar
watch(() => route.params.id, loadLesson)

// Encontrar a próxima e a lição anterior
const currentIndex = computed(() => lessons.value.findIndex(l => l.id === lesson.value?.id))
const previousLesson = computed(() => (currentIndex.value > 0 ? lessons.value[currentIndex.value - 1] : null))
const nextLesson = computed(() => (currentIndex.value < lessons.value.length - 1 ? lessons.value[currentIndex.value + 1] : null))
</script>

<template>
  <div class="container">
    <h1>{{ lesson?.title }}</h1>

    <div v-if="lesson?.content.sections">
      <template v-for="(section, index) in lesson.content.sections" :key="index">
        
        <!-- Renderiza Texto -->
        <p v-if="section.type === 'text'">{{ section.content }}</p>

        <!-- Renderiza Imagem -->
        <div v-if="section.type === 'image'" class="image-container">
          <img :src="section.url" :alt="section.caption" />
          <p class="caption">{{ section.caption }}</p>
        </div>

        <!-- Renderiza Vídeo -->
        <div v-if="section.type === 'video'" class="video-container">
          <iframe width="100%" height="315" :src="section.url" frameborder="0" allowfullscreen></iframe>
        </div>

        <!-- Renderiza Lista -->
        <ul v-if="section.type === 'list'">
          <li v-for="(item, i) in section.items" :key="i">{{ item }}</li>
        </ul>
        
      </template>
    </div>

    <!-- Botão para Marcar como Concluído -->
    <button v-if="!isLessonCompleted" class="complete-button" @click="markAsCompleted">
      ✅ Mark as Completed
    </button>

    <p v-if="isLessonCompleted" class="completed-message">
      🎉 Lesson Completed!
    </p>

    <!-- Navegação entre lições -->
    <div class="navigation-buttons">
      <button v-if="previousLesson" @click="router.push(`/lesson/${previousLesson.id}`)">
        ⬅ Previous Lesson
      </button>
      
      <button v-if="nextLesson" @click="router.push(`/lesson/${nextLesson.id}`)">
        Next Lesson ➡
      </button>
    </div>

    <router-link :to="`/learning-path/${lesson?.learning_path_id}`">
      <button class="back-button">⬅ Back to Course</button>
    </router-link>
  </div>
</template>

<style scoped>
.container {
  max-width: 700px;
  margin: auto;
  padding: 20px;
}

h1 {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 10px;
}

p {
  font-size: 1.2rem;
  text-align: center;
}

.image-container {
  text-align: center;
  margin: 15px 0;
}

.image-container img {
  max-width: 100%;
  border-radius: 8px;
}

.caption {
  font-style: italic;
  color: #555;
}

.video-container {
  text-align: center;
  margin: 20px 0;
}

ul {
  list-style-type: disc;
  margin: 15px;
  padding-left: 20px;
  font-size: 1.1rem;
}

/* Botão de Concluir */
.complete-button {
  display: block;
  margin: 20px auto;
  background: #28a745;
  color: white;
  padding: 12px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.complete-button:hover {
  background: #218838;
}

/* Mensagem de Concluído */
.completed-message {
  text-align: center;
  font-size: 1.2rem;
  color: #28a745;
  font-weight: bold;
  margin-top: 10px;
}

button {
  background: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 10px;
  font-size: 1rem;
}

button:hover {
  background: #0056b3;
}

.back-button {
  display: block;
  margin: 20px auto;
  text-align: center;
  background: #6c757d;
}

.back-button:hover {
  background: #5a6268;
}

.navigation-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
</style>
