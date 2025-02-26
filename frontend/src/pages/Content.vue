<script setup>
import { ref } from 'vue'
import ArticleCard from '../components/ArticleCard.vue'

// Dados fictícios para teste
const articles = ref([
  {
    id: 1,
    title: 'Introduction to Guitar Chords',
    description: 'Learn the basics of guitar chords and how to switch between them smoothly.',
    image: 'https://source.unsplash.com/400x250/?guitar,music'
  },
  {
    id: 2,
    title: 'Piano for Beginners',
    description: 'A step-by-step guide to getting started with the piano.',
    image: 'https://source.unsplash.com/400x250/?piano,music'
  },
  {
    id: 3,
    title: 'The Benefits of Learning an Instrument',
    description: 'Discover how playing an instrument can improve cognitive skills and mental health.',
    image: 'https://source.unsplash.com/400x250/?music,instrument'
  },
  {
    id: 4,
    title: 'The Benefits of Learning an Instrument',
    description: 'Discover how playing an instrument can improve cognitive skills and mental health.',
    image: 'https://source.unsplash.com/400x250/?music,instrument'
  }
])
</script>

<template>
  <div class="container">
    <h1>Music Content 🎼</h1>
    <p>Explore our collection of music tutorials and articles.</p>

    <div class="articles">
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
</style>
