<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import InstrumentModal from '../components/InstrumentModal.vue'

const router = useRouter()
const user = ref({
  username: '',
  email: '',
  dateOfBirth: '',
  bio: '',
  authProvider: 'local', // Pode ser 'local' ou 'google'
  profilePicture: '',
  instruments: [] // Lista de instrumentos do usuário
})
const isEditing = ref(false)
const isModalOpen = ref(false) // Controla a abertura do modal

// Simula carregamento de usuário e instrumentos do LocalStorage
onMounted(() => {
  const storedUser = JSON.parse(localStorage.getItem('user'))
  if (storedUser) {
    user.value = storedUser
    user.value.instruments = JSON.parse(localStorage.getItem('userInstruments')) || []
  } else {
    router.push('/login') // Redireciona para login se não estiver autenticado
  }
})

// Salvar alterações no perfil
const saveProfile = () => {
  localStorage.setItem('user', JSON.stringify(user.value))
  isEditing.value = false
}

// Processa o upload da imagem de perfil
const handleProfilePictureUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = () => {
      user.value.profilePicture = reader.result
    }
    reader.readAsDataURL(file)
  }
}

// Remover um instrumento do usuário
const removeInstrument = (id) => {
  user.value.instruments = user.value.instruments.filter(inst => inst.id !== id)
  localStorage.setItem('userInstruments', JSON.stringify(user.value.instruments))
}

// Adicionar novo instrumento via modal
const addInstrument = (newInstrument) => {
  newInstrument.id = Date.now().toString() // Gera um ID único
  if (!newInstrument.image) {
    newInstrument.image = 'https://source.unsplash.com/200x150/?instrument' // Imagem padrão
  }
  user.value.instruments.push(newInstrument)
  localStorage.setItem('userInstruments', JSON.stringify(user.value.instruments))
}
</script>

<template>
  <div class="profile-container">
    <h1>Meu Perfil</h1>

    <div class="profile-card">
      <div v-if="user.profilePicture" class="profile-picture">
        <img :src="user.profilePicture" alt="Profile Picture" />
      </div>
      <input type="file" accept="image/*" @change="handleProfilePictureUpload" v-if="isEditing" />

      <div class="profile-info">
        <label>Nome de Usuário:</label>
        <input v-if="isEditing" v-model="user.username" type="text" />
        <p v-else>{{ user.username }}</p>

        <label>Email:</label>
        <p>{{ user.email }}</p>

        <label>Data de Nascimento:</label>
        <input v-if="isEditing" v-model="user.dateOfBirth" type="date" />
        <p v-else>{{ user.dateOfBirth || 'Não informado' }}</p>

        <label>Sobre Mim:</label>
        <textarea v-if="isEditing" v-model="user.bio" placeholder="Fale um pouco sobre você..."></textarea>
        <p v-else>{{ user.bio || 'Nenhuma bio cadastrada' }}</p>

        <label>Autenticação:</label>
        <p>{{ user.authProvider === 'google' ? 'Google SSO' : 'Cadastro Local' }}</p>

        <div class="profile-actions">
          <button v-if="isEditing" @click="saveProfile">Salvar</button>
          <button v-if="!isEditing" @click="isEditing = true">Editar</button>
          <button @click="router.push('/instrument-wall')">Ver Mural</button>
          <button @click="router.push('/login')" class="logout-button">Logout</button>
        </div>
      </div>
    </div>

    <!-- Seção de Instrumentos do Usuário -->
    <div class="instruments-section">
      <h2>🎸 Meus Instrumentos</h2>
      <button @click="isModalOpen = true" class="add-button">+ Adicionar Instrumento</button>

      <div v-if="user.instruments.length > 0" class="instrument-list">
        <div v-for="instrument in user.instruments" :key="instrument.id" class="instrument-card">
          <img :src="instrument.image" alt="Instrument Image" />
          <h3>{{ instrument.name }}</h3>
          <p>{{ instrument.description }}</p>
          <button @click="removeInstrument(instrument.id)" class="remove-button">Remover</button>
        </div>
      </div>
      <p v-else class="no-instruments">Nenhum instrumento cadastrado.</p>
    </div>

    <!-- Modal de Adicionar Instrumento -->
    <InstrumentModal v-if="isModalOpen" @close="isModalOpen = false" @add-instrument="addInstrument" />
  </div>
</template>

<style scoped>
/* Estrutura da Página */
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

input, textarea {
  width: 100%;
  padding: 10px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 5px;
}

textarea {
  resize: vertical;
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

/* Estilização da Seção de Instrumentos */
.instruments-section {
  margin-top: 30px;
  text-align: center;
}

.add-button {
  background: #28a745;
  margin-bottom: 15px;
}

.add-button:hover {
  background: #1e7e34;
}

.instrument-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
}

.instrument-card {
  background: white;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  width: 250px;
}

.instrument-card img {
  width: 100%;
  border-radius: 8px;
}

.instrument-card h3 {
  margin: 10px 0;
}

.remove-button {
  background: #dc3545;
  margin-top: 10px;
}

.remove-button:hover {
  background: #a71d2a;
}

.no-instruments {
  font-size: 1.1rem;
  color: #777;
  margin-top: 15px;
}
</style>
