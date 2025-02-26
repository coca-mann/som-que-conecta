<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const isLoading = ref(true) // Estado de carregamento
const article = ref(null)

const articles = [
  {
    id: 1,
    title: 'Introduction to Guitar Chords',
    content: 'Learning guitar chords is fundamental for playing songs...',
    image: 'https://source.unsplash.com/800x400/?guitar,music'
  },
  {
    id: 2,
    title: 'Piano for Beginners',
    content: 'The piano is one of the easiest instruments to start with...',
    image: 'https://source.unsplash.com/800x400/?piano,music'
  },
  {
    id: 3,
    title: 'The Benefits of Learning an Instrument',
    content: 'Music can improve cognitive skills, mental health, and more...',
    image: 'https://source.unsplash.com/800x400/?music,instrument'
  }
]

const route = useRoute()

onMounted(() => {
  const articleId = parseInt(route.params.id)
  article.value = articles.find(a => a.id === articleId)

  // Simulando um atraso no carregamento
  setTimeout(() => {
    isLoading.value = false
  }, 1500) // Aguarda 1.5 segundos antes de exibir o conteúdo
})
</script>

<template>
  <div class="container">
    <!-- Exibe o carregamento -->
    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading article...</p>
    </div>

    <!-- Exibe o artigo quando carregar -->
    <div v-else>
      <img :src="article.image" alt="Article Image" class="article-image" />
      <h1>{{ article.title }}</h1>
      <p>{{ article.content }}</p>
      <router-link to="/content">
        <button>Back to Articles</button>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.article-image {
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

p {
  font-size: 1.2rem;
  line-height: 1.6;
  color: #444;
}

button {
  display: block;
  margin: 20px auto;
  padding: 10px 15px;
  background: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  transition: background 0.2s;
}

button:hover {
  background: #0056b3;
}

/* Estilo do carregamento */
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
</style>
