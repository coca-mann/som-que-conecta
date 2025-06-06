<template>
  <div class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-900">
          {{ instrument ? 'Editar Instrumento' : 'Adicionar Instrumento' }}
        </h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
          <X class="h-6 w-6" />
        </button>
      </div>
      
      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Image Upload -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Foto do Instrumento</label>
          <div class="flex items-center gap-4">
            <div class="w-32 h-32 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center bg-gray-50">
              <img v-if="form.image" :src="form.image" alt="Preview" class="w-full h-full object-cover rounded-lg">
              <div v-else class="text-center">
                <Camera class="h-8 w-8 text-gray-400 mx-auto mb-2" />
                <span class="text-sm text-gray-500">Foto</span>
              </div>
            </div>
            <div class="flex-1">
              <input 
                type="url" 
                v-model="form.image" 
                placeholder="URL da imagem do instrumento"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
              <p class="text-xs text-gray-500 mt-1">Cole a URL de uma imagem do instrumento</p>
            </div>
          </div>
        </div>

        <!-- Basic Information -->
        <div class="grid md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nome do Instrumento *</label>
            <input 
              v-model="form.name" 
              type="text" 
              required 
              placeholder="Ex: Violão Clássico Yamaha C40"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tipo *</label>
            <select 
              v-model="form.type" 
              required 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Selecione o tipo</option>
              <option value="Cordas">Cordas</option>
              <option value="Sopro">Sopro</option>
              <option value="Percussão">Percussão</option>
              <option value="Teclas">Teclas</option>
            </select>
          </div>
        </div>

        <div class="grid md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Marca *</label>
            <input 
              v-model="form.brand" 
              type="text" 
              required 
              placeholder="Ex: Yamaha, Fender, Pearl"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Cor</label>
            <div class="flex gap-2">
              <input 
                v-model="form.color" 
                type="color" 
                class="w-12 h-10 border border-gray-300 rounded cursor-pointer"
              >
              <input 
                v-model="form.colorName" 
                type="text" 
                placeholder="Nome da cor"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
            </div>
          </div>
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Descrição *</label>
          <textarea 
            v-model="form.description" 
            rows="4" 
            required
            placeholder="Descreva as características, condições e especificações do instrumento..."
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          ></textarea>
        </div>

        <!-- Location and Hours -->
        <div class="grid md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Localização *</label>
            <input 
              v-model="form.location" 
              type="text" 
              required 
              placeholder="Ex: Centro - Sala 101"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Horários Disponíveis *</label>
            <input 
              v-model="form.availableHours" 
              type="text" 
              required 
              placeholder="Ex: Seg-Sex: 14h-18h"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
          </div>
        </div>

        <!-- Submit Buttons -->
        <div class="flex justify-end gap-3 pt-4 border-t">
          <button 
            type="button" 
            @click="$emit('close')" 
            class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
          >
            Cancelar
          </button>
          <button 
            type="submit" 
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            {{ instrument ? 'Atualizar' : 'Adicionar' }} Instrumento
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { X, Camera } from 'lucide-vue-next'

const props = defineProps({
  instrument: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'saved'])

const form = ref({
  name: '',
  type: '',
  brand: '',
  color: '#000000',
  colorName: '',
  description: '',
  location: '',
  availableHours: '',
  image: ''
})

const handleSubmit = () => {
  emit('saved', { ...form.value })
}

onMounted(() => {
  if (props.instrument) {
    Object.assign(form.value, props.instrument)
  }
})
</script>