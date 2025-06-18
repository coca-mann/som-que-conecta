<template>
  <div class="fixed inset-0 backdrop-blur-sm bg-black/30 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4 shadow-xl">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-900">
          Cadastrar
        </h2>
        <button
          class="text-gray-400 hover:text-gray-600"
          @click="$emit('close')"
        >
          <X class="h-6 w-6" />
        </button>
      </div>
      
      <form
        class="space-y-4"
        @submit.prevent="handleRegister"
      >
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nome Completo</label>
          <input
            v-model="form.name"
            type="text"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input
            v-model="form.email"
            type="email"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Senha</label>
          <input
            v-model="form.password"
            type="password"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Confirmar Senha</label>
          <input
            v-model="form.confirmPassword"
            type="password"
            required
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Usuário</label>
          <select
            v-model="form.role"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="student">
              Estudante
            </option>
            <option value="teacher">
              Professor
            </option>
          </select>
        </div>
        
        <div class="flex items-center">
          <input
            v-model="form.acceptTerms"
            type="checkbox"
            required
            class="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          >
          <span class="ml-2 text-sm text-gray-600">
            Aceito os <a
              href="#"
              class="text-blue-600 hover:text-blue-800"
            >termos de uso</a> e 
            <a
              href="#"
              class="text-blue-600 hover:text-blue-800"
            >política de privacidade</a>
          </span>
        </div>
        
        <button
          type="submit"
          :disabled="!isFormValid"
          class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          Cadastrar
        </button>
      </form>
      
      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">
          Já tem uma conta? 
          <button
            class="text-blue-600 hover:text-blue-800 font-medium"
            @click="switchToLogin"
          >
            Faça login
          </button>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { X } from 'lucide-vue-next'

const emit = defineEmits(['close', 'register', 'switch-to-login'])

const form = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: 'student',
  acceptTerms: false
})

const isFormValid = computed(() => {
  return form.value.name && 
         form.value.email && 
         form.value.password && 
         form.value.password === form.value.confirmPassword &&
         form.value.acceptTerms
})

const handleRegister = () => {
  if (!isFormValid.value) return
  
  // Here you would typically validate and send to your backend
  const userData = {
    name: form.value.name,
    email: form.value.email,
    role: form.value.role
  }
  
  emit('register', userData)
}

const switchToLogin = () => {
  emit('close')
  // You could emit a different event to switch modals
}
</script>