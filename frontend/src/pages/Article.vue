<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

// Simulação de dados (futuramente será substituído por API ou Vuex/Pinia)
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
const article = ref(null)

onMounted(() => {
  const articleId = parseInt(route.params.id)
  article.value = articles.find(a => a.id === articleId)
})
</script>

<template>
  <div class="container" v-if="article">
    <img :src="article.image" alt="Article Image" class="article-image" />
    <h1>{{ article.title }}</h1>
    <p>{{ article.content }}</p>
    <router-link to="/content">
      <button>Back to Articles</button>
    </router-link>
  </div>
  <div v-else class="container">
    <h1>Article not found</h1>
    <router-link to="/content">
      <button>Back to Articles</button>
    </router-link>
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
</style>
