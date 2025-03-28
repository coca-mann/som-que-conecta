<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const username = ref('')
const password = ref('')
const errorMessage = ref('')

const handleLogin = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/token/', {
      username: username.value,
      password: password.value
    })

    // Armazena os tokens JWT
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)

    // Redireciona para a home
    router.push('/')
  } catch (error) {
    if (error.response && error.response.status === 401) {
      errorMessage.value = 'Usuário ou senha inválidos.'
    } else {
      errorMessage.value = 'Erro ao conectar com o servidor.'
    }
  }
}

const handleGoogleLogin = () => {
  alert('Google SSO ainda não está configurado. Isso será integrado ao backend!')
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Login</h1>

      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <form @submit.prevent="handleLogin">
        <label for="username">Usuário</label>
        <input v-model="username" type="text" id="username" placeholder="Digite seu usuário" required />

        <label for="password">Senha</label>
        <input v-model="password" type="password" id="password" placeholder="Digite sua senha" required />

        <button type="submit">Entrar</button>
      </form>

      <div class="divider">ou</div>

      <button class="google-button" @click="handleGoogleLogin">
        <img src="https://user-images.githubusercontent.com/700503/58114684-e12ffd00-7c2a-11e9-8d59-4ab1c501afe8.jpg" alt="Google Logo" />
        Entrar com Google
      </button>

      <p class="register-link">Ainda não tem conta? <router-link to="/register">Cadastre-se aqui</router-link></p>
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

/* Link para registro */
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
