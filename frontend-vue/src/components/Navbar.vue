<script setup>
import { ref, onMounted } from 'vue'

const isAuthenticated = ref(false)
const user = ref(null)

onMounted(() => {
  // Criar um usuário fixo para testes
  const testUser = {
    name: 'John Doe',
    email: 'johndoe@example.com',
    profilePicture: 'https://i.pravatar.cc/100' // Avatar de teste
  }

  if (!localStorage.getItem('user')) {
    localStorage.setItem('user', JSON.stringify(testUser)) // Salva usuário no localStorage
  }

  user.value = JSON.parse(localStorage.getItem('user'))
  isAuthenticated.value = !!user.value
})
</script>

<template>
  <nav>
    <div class="container">
      <ul class="nav-links">
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/content">Content</router-link></li>
        <li><router-link to="/instrument-wall">Instrument Wall</router-link></li>
        <li><router-link to="/learning">Mini Courses</router-link></li>
        <li><router-link to="/about">About</router-link></li>
      </ul>

      <!-- Avatar do Usuário à Direita -->
      <div v-if="isAuthenticated" class="user-avatar">
        <router-link to="/profile">
          <img :src="user.profilePicture" alt="User Avatar" />
        </router-link>
      </div>

      <div v-else>
        <router-link to="/login" class="login-button">Login</router-link>
      </div>
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
  margin: auto;
  padding: 0 20px;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 20px;
}

.nav-links li {
  margin: 0;
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

/* Avatar */
.user-avatar {
  display: flex;
  align-items: center;
}

.user-avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid white;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.user-avatar img:hover {
  transform: scale(1.1);
}

/* Botão de Login */
.login-button {
  background: white;
  color: #007bff;
  padding: 8px 15px;
  border-radius: 5px;
  text-decoration: none;
  font-weight: bold;
  transition: background 0.2s ease-in-out, color 0.2s;
}

.login-button:hover {
  background: #0056b3;
  color: white;
}
</style>
