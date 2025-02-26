<script setup>
</script>

<template>
  <nav>
    <ul>
      <li><router-link to="/">Home</router-link></li>
      <li><router-link to="/content">Content</router-link></li>
      <li><router-link to="/instrument-wall">Instrument Wall</router-link></li>
      <li><router-link to="/about">About</router-link></li>
    </ul>
  </nav>
</template>

<style scoped>
nav {
  background: #007bff;
  padding: 10px;
  text-align: center;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
}

li {
  margin: 0 15px;
}

a {
  color: white;
  text-decoration: none;
  font-weight: bold;
}

a:hover {
  text-decoration: underline;
}
</style>
