<script setup>
defineProps({
  article: Object
})
</script>

<template>
  <div class="article-card">
    <img :src="article.content.media[0].url" alt="Article Image" />
    <h2>{{ article.title }}</h2>
    <p>{{ article.content.text.substring(0, 100) }}...</p>
    <router-link :to="`/article/${article.id}`">
      <button>Read More</button>
    </router-link>
  </div>
</template>

<style scoped>
.article-card {
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.2s ease-in-out;
}

.article-card:hover {
  transform: scale(1.02);
}

img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: 6px;
}

h2 {
  font-size: 1.4rem;
  margin: 10px 0;
}

p {
  font-size: 1rem;
  color: #555;
}

button {
  background: #007bff;
  color: white;
  border: none;
  padding: 8px 12px;
  margin-top: 10px;
  cursor: pointer;
  border-radius: 5px;
  transition: background 0.2s;
}

button:hover {
  background: #0056b3;
}
</style>
