<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const isLoading = ref(true)
const article = ref(null)

onMounted(async () => {
  try {
    const response = await fetch('/data/articles.json') // Carrega o JSON
    const articles = await response.json()

    const articleId = route.params.id
    article.value = articles.find(a => a.id === articleId)

    if (!article.value) {
      console.warn(`Article with ID ${articleId} not found.`)
      router.push('/content') // Redireciona para a lista se o artigo não existir
      return
    }

  } catch (error) {
    console.error('Error loading article:', error)
  } finally {
    setTimeout(() => {
      isLoading.value = false
    }, 1000) // Simula carregamento
  }
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
    <div v-else-if="article">
      <img :src="article.content.media[0]?.url" alt="Article Image" class="article-image" />
      <h1>{{ article.title }}</h1>
      <p>{{ article.content.text }}</p>
      <router-link to="/content">
        <button>Back to Articles</button>
      </router-link>
    </div>

    <!-- Exibe mensagem se o artigo não for encontrado -->
    <div v-else class="error-container">
      <h1>Article not found</h1>
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

.error-container {
  text-align: center;
  color: red;
  margin-top: 50px;
}
</style>
