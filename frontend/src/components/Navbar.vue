<script setup>
</script>

<template>
  <nav>
    <div class="container">
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/content">Content</router-link></li>
        <li><router-link to="/instrument-wall">Instrument Wall</router-link></li>
        <li><router-link to="/about">About</router-link></li>
      </ul>
    </div>
  </nav>
</template>

<style scoped>
nav {
  background: #007bff;
  padding: 15px 0;
}

ul {
  display: flex;
  justify-content: center;
  list-style: none;
}

li {
  margin: 0 20px;
}

a {
  color: white;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: bold;
}

a:hover {
  text-decoration: underline;
}
</style>
