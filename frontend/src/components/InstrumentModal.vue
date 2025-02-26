<script setup>
import { ref, defineEmits, onMounted } from 'vue'

const emits = defineEmits(['close', 'add-instrument'])

// Dados do instrumento a ser cadastrado
const instrument = ref({
  instrumentType: '',
  color: '',
  brand: '',
  description: '',
  isAvailable: true,
  location: '',
  image: ''
})

// Lista fixa de tipos de instrumentos (Simulação, futuramente será carregado do backend)
const instrumentTypes = ref([])

onMounted(() => {
  // Simulação de tipos de instrumentos cadastrados previamente
  instrumentTypes.value = [
    { id: '1', name: 'Violão' },
    { id: '2', name: 'Guitarra' },
    { id: '3', name: 'Piano' },
    { id: '4', name: 'Teclado' },
    { id: '5', name: 'Bateria' }
  ]
})

// Processa o upload da imagem e converte para Base64
const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = () => {
      instrument.value.image = reader.result
    }
    reader.readAsDataURL(file)
  }
}

// Salva o instrumento e fecha o modal
const saveInstrument = () => {
  if (!instrument.value.instrumentType || !instrument.value.color || !instrument.value.brand || !instrument.value.description) {
    alert('Preencha todos os campos obrigatórios!')
    return
  }
  emits('add-instrument', instrument.value)
  emits('close')
}
</script>

<template>
  <div class="modal-overlay" @click.self="emits('close')">
    <div class="modal">
      <h2>Adicionar Novo Instrumento</h2>

      <label>Tipo de Instrumento:</label>
      <select v-model="instrument.instrumentType" required>
        <option value="" disabled>Selecione um tipo</option>
        <option v-for="type in instrumentTypes" :key="type.id" :value="type.name">{{ type.name }}</option>
      </select>

      <label>Cor:</label>
      <input v-model="instrument.color" type="text" placeholder="Ex: Marrom, Preto..." required />

      <label>Marca:</label>
      <input v-model="instrument.brand" type="text" placeholder="Ex: Yamaha, Fender..." required />

      <label>Descrição:</label>
      <textarea v-model="instrument.description" placeholder="Descreva o instrumento..." required></textarea>

      <label>Disponível para Empréstimo?</label>
      <select v-model="instrument.isAvailable">
        <option :value="true">Sim</option>
        <option :value="false">Não</option>
      </select>

      <label v-if="instrument.isAvailable">Localização (ONGs):</label>
      <input v-if="instrument.isAvailable" v-model="instrument.location" type="text" placeholder="Informe o local (opcional)" />

      <label>Imagem do Instrumento:</label>
      <input type="file" accept="image/*" @change="handleImageUpload" />

      <!-- Pré-visualização da Imagem -->
      <div v-if="instrument.image" class="image-preview">
        <img :src="instrument.image" alt="Instrument Preview" />
      </div>

      <div class="modal-actions">
        <button @click="saveInstrument">Salvar</button>
        <button class="cancel-button" @click="emits('close')">Cancelar</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
  text-align: center;
}

label {
  display: block;
  text-align: left;
  font-weight: bold;
  margin-top: 10px;
}

input, select, textarea {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

textarea {
  resize: vertical;
}

.image-preview {
  margin-top: 10px;
  text-align: center;
}

.image-preview img {
  max-width: 100%;
  max-height: 150px;
  border-radius: 5px;
  box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.2);
}

.modal-actions {
  margin-top: 15px;
  display: flex;
  justify-content: space-between;
}

button {
  background: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background: #0056b3;
}

.cancel-button {
  background: #dc3545;
}

.cancel-button:hover {
  background: #a71d2a;
}
</style>
