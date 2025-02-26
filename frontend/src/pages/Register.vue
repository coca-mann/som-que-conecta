<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const name = ref('')
const email = ref('')
const password = ref('')
const errorMessage = ref('')

const handleRegister = () => {
  if (!name.value || !email.value || !password.value) {
    errorMessage.value = 'All fields are required.'
    return
  }

  // Simulação de registro (depois será integrado ao backend)
  console.log(`User registered: ${name.value}, ${email.value}`)
  router.push('/')
}

// Simula login via Google (SSO) - Será integrado ao backend futuramente
const handleGoogleLogin = () => {
  console.log('Google Login initiated')
  alert('Google SSO ainda não está configurado. Isso será integrado ao backend!')
}
</script>

<template>
  <div class="register-container">
    <div class="register-card">
      <h1>Register</h1>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <form @submit.prevent="handleRegister">
        <label for="name">Full Name</label>
        <input v-model="name" type="text" id="name" placeholder="Enter your full name" required />

        <label for="email">Email</label>
        <input v-model="email" type="email" id="email" placeholder="Enter your email" required />

        <label for="password">Password</label>
        <input v-model="password" type="password" id="password" placeholder="Enter your password" required />

        <button type="submit">Sign Up</button>
      </form>

      <div class="divider">or</div>

      <!-- Botão para SSO do Google -->
      <button class="google-button" @click="handleGoogleLogin">
        <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" alt="Google Logo" />
        Sign Up with Google
      </button>

      <p class="login-link">Already have an account? <router-link to="/login">Login here</router-link></p>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f4f4f4;
}

.register-card {
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

/* Divisor entre opções */
.divider {
  margin: 15px 0;
  font-size: 1rem;
  color: #777;
}

/* Botão Google SSO */
.google-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border: 1px solid #ccc;
  color: #333;
  padding: 10px;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
}

.google-button img {
  width: 20px;
  margin-right: 10px;
}

.google-button:hover {
  background: #f1f1f1;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

/* Mensagem de erro */
.error-message {
  color: red;
  margin-bottom: 10px;
}

/* Link para login */
.login-link {
  margin-top: 10px;
  font-size: 0.9rem;
}

.login-link a {
  color: #007bff;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
