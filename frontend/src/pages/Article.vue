<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CommentSection from '../components/CommentSection.vue'

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
      router.push('/content')
      return
    }

  } catch (error) {
    console.error('Error loading article:', error)
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
      <p>Loading article...</p>
    </div>

    <div v-else-if="article">
      <img :src="article.content.media[0]?.url" alt="Article Image" class="article-image" />
      <h1>{{ article.title }}</h1>
      <p>{{ article.content.text }}</p>
      
      <!-- Seção de Comentários -->
      <CommentSection :comments="article.comments || []" />

      <router-link to="/content">
        <button>Back to Articles</button>
      </router-link>
    </div>

    <div v-else class="error-container">
      <h1>Article not found</h1>
      <router-link to="/content">
        <button>Back to Articles</button>
      </router-link>
    </div>
  </div>
</template>
