<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref({
  name: '',
  email: '',
  profilePicture: '' // Opcional: Imagem de perfil
})
const isEditing = ref(false)

// Simula carregamento de usuário (depois será integrado ao backend)
onMounted(() => {
  const storedUser = JSON.parse(localStorage.getItem('user'))
  if (storedUser) {
    user.value = storedUser
  } else {
    router.push('/login') // Redireciona para login se não estiver autenticado
  }
})

// Salvar alterações
const saveProfile = () => {
  localStorage.setItem('user', JSON.stringify(user.value))
  isEditing.value = false
}

// Logout
const logout = () => {
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<template>
  <div class="profile-container">
    <h1>Meu Perfil</h1>

    <div class="profile-card">
      <div v-if="user.profilePicture" class="profile-picture">
        <img :src="user.profilePicture" alt="Profile Picture" />
      </div>

      <div class="profile-info">
        <label>Nome:</label>
        <input v-if="isEditing" v-model="user.name" type="text" />
        <p v-else>{{ user.name }}</p>

        <label>Email:</label>
        <input v-if="isEditing" v-model="user.email" type="email" />
        <p v-else>{{ user.email }}</p>

        <div class="profile-actions">
          <button v-if="isEditing" @click="saveProfile">Salvar</button>
          <button v-if="!isEditing" @click="isEditing = true">Editar</button>
          <button @click="logout" class="logout-button">Logout</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 20px;
  text-align: center;
  background: white;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.profile-card {
  display: flex;
  align-items: center;
  flex-direction: column;
}

.profile-picture img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 15px;
  object-fit: cover;
}

.profile-info {
  width: 100%;
}

label {
  display: block;
  font-weight: bold;
  margin-top: 10px;
}

input {
  width: 100%;
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

p {
  font-size: 1.2rem;
  color: #555;
  margin: 5px 0;
}

.profile-actions {
  margin-top: 15px;
}

button {
  background: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 5px;
}

button:hover {
  background: #0056b3;
}

.logout-button {
  background: #dc3545;
}

.logout-button:hover {
  background: #a71d2a;
}
</style>
