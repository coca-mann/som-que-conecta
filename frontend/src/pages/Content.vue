<script setup>
import { ref, onMounted } from 'vue'
import ArticleCard from '../components/ArticleCard.vue'

const articles = ref([])
const isLoading = ref(true)

onMounted(async () => {
  try {
    const response = await fetch('/data/articles.json') // Busca o JSON
    articles.value = await response.json()
  } catch (error) {
    console.error('Failed to load articles:', error)
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="container">
    <h1>Music Content 🎼</h1>
    <p>Explore our collection of music tutorials and articles.</p>

    <!-- Exibe o carregamento -->
    <div v-if="isLoading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading articles...</p>
    </div>

    <!-- Exibe os artigos -->
    <div v-else class="articles">
      <ArticleCard v-for="article in articles" :key="article.id" :article="article" />
    </div>
  </div>
</template>

<style scoped>
.articles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
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
