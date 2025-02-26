<script setup>
import { ref, computed, onMounted } from 'vue'
import ArticleCard from '../components/ArticleCard.vue'

const articles = ref([]) // Lista original de artigos
const searchQuery = ref('') // Texto digitado na busca
const selectedTag = ref('All') // Tag selecionada para filtro
const uniqueTags = ref([]) // Lista única de tags disponíveis

onMounted(async () => {
  try {
    const response = await fetch('/data/articles.json') // Carrega os artigos
    articles.value = await response.json()

    // Coleta todas as tags únicas dos artigos
    const allTags = articles.value.flatMap(article => article.tags || [])
    uniqueTags.value = ['All', ...new Set(allTags)] // Remove duplicatas e adiciona "All"
  } catch (error) {
    console.error('Failed to load articles:', error)
  }
})

// Filtra os artigos conforme a busca e a tag selecionada
const filteredArticles = computed(() => {
  return articles.value.filter(article => {
    const matchesSearch = article.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchesTag = selectedTag.value === 'All' || (article.tags && article.tags.includes(selectedTag.value))
    return matchesSearch && matchesTag
  })
})
</script>

<template>
  <div class="container">
    <h1>Music Content 🎼</h1>
    <p>Explore our collection of music tutorials and articles.</p>

    <!-- Barra de Pesquisa e Filtros -->
    <div class="filters">
      <input v-model="searchQuery" type="text" placeholder="Search articles..." />

      <select v-model="selectedTag">
        <option v-for="tag in uniqueTags" :key="tag" :value="tag">{{ tag }}</option>
      </select>
    </div>

    <!-- Exibe os artigos filtrados -->
    <div class="articles">
      <ArticleCard v-for="article in filteredArticles" :key="article.id" :article="article" />
    </div>

    <!-- Caso não encontre nenhum artigo -->
    <div v-if="filteredArticles.length === 0" class="no-results">
      <p>No articles found matching your criteria.</p>
    </div>
  </div>
</template>

<style scoped>
/* Estilização dos filtros */
.filters {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  gap: 10px;
}

.filters input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
}

.filters select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
  background: white;
}

/* Grid de artigos */
.articles {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

/* Mensagem quando nenhum artigo for encontrado */
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
