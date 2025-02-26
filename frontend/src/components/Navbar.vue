<script setup>
import { ref, onMounted } from 'vue'

const isAuthenticated = ref(false)

onMounted(() => {
  // Criar um usuário fixo para testes
  const testUser = {
    name: 'John Doe',
    email: 'johndoe@example.com',
    profilePicture: 'https://i.pravatar.cc/100' // Avatar de teste
  }

  if (!localStorage.getItem('user')) {
    localStorage.setItem('user', JSON.stringify(testUser)) // Define usuário fixo
  }

  isAuthenticated.value = true
})
</script>

<template>
  <nav>
    <div class="container">
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/content">Content</router-link></li>
        <li><router-link to="/instrument-wall">Instrument Wall</router-link></li>
        <li><router-link to="/about">About</router-link></li>
        <li v-if="isAuthenticated"><router-link to="/profile">Profile</router-link></li>
        <li v-else><router-link to="/login">Login</router-link></li>
      </ul>
      <ThemeSwitcher />
    </div>
  </nav>
</template>


<style scoped>
nav {
  background: #007bff;
  padding: 15px 0;
}

.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

ul {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
}

li {
  margin: 0 15px;
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

/* Botão de Login */
.login-button {
  background: white;
  color: #007bff;
  padding: 8px 15px;
  border-radius: 5px;
  font-weight: bold;
  transition: background 0.2s ease-in-out, color 0.2s ease-in-out;
}

.login-button:hover {
  background: #f1f1f1;
}
</style>
