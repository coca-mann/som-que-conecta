<script setup>
defineProps({
  instrument: Object
})
</script>

<template>
    <router-link :to="`/instrument/${instrument.id}`" class="instrument-card">
      <img :src="instrument.image" alt="Instrument Image" />
      <h2>{{ instrument.name }}</h2>
      <p>{{ instrument.description }}</p>
      <p class="location">📍 {{ instrument.location }}</p>
      <span class="status" :class="{ available: instrument.status === 'Available', unavailable: instrument.status !== 'Available' }">
        {{ instrument.status }}
      </span>
    </router-link>
  </template>
  

<style scoped>
.instrument-card {
  background: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.2s ease-in-out;
}

.instrument-card:hover {
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

.location {
  font-size: 0.9rem;
  color: #007bff;
  margin-top: 5px;
}

.status {
  display: inline-block;
  margin-top: 10px;
  padding: 5px 10px;
  border-radius: 5px;
  font-weight: bold;
}

.available {
  background: #28a745;
  color: white;
}

.unavailable {
  background: #dc3545;
  color: white;
}
</style>
