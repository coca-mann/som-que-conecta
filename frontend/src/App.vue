<script setup>
</script>

<template>
  <div>
    <nav>
      <router-link to="/">Home</router-link>
    </nav>

    <router-view />
  </div>
</template>

<style scoped>
nav {
  text-align: center;
  margin-bottom: 20px;
}

nav a {
  text-decoration: none;
  color: #007bff;
  font-weight: bold;
  margin: 0 10px;
}

nav a:hover {
  text-decoration: underline;
}
</style>
