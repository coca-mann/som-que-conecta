<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const password = ref('')
const errorMessage = ref('')

const handleLogin = () => {
  // Simulação de autenticação (posteriormente será integrado com backend)
  if (email.value === 'user@example.com' && password.value === '123456') {
    router.push('/') // Redireciona para a home após login bem-sucedido
  } else {
    errorMessage.value = 'Invalid email or password. Try again.'
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Login</h1>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <form @submit.prevent="handleLogin">
        <label for="email">Email</label>
        <input v-model="email" type="email" id="email" placeholder="Enter your email" required />

        <label for="password">Password</label>
        <input v-model="password" type="password" id="password" placeholder="Enter your password" required />

        <button type="submit">Sign In</button>
      </form>

      <p class="register-link">Don't have an account? <router-link to="/register">Register here</router-link></p>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f4f4f4;
}

.login-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 100%;
  max-width: 400px;
}

h1 {
  margin-bottom: 15px;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  text-align: left;
  font-weight: bold;
  margin-bottom: 5px;
}

input {
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 1rem;
}

button {
  background: #007bff;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover {
  background: #0056b3;
}

.error-message {
  color: red;
  margin-bottom: 10px;
}

.register-link {
  margin-top: 10px;
  font-size: 0.9rem;
}

.register-link a {
  color: #007bff;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>
