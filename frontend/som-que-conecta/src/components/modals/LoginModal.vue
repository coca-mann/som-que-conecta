<template>
  <div class="fixed inset-0 backdrop-blur-sm bg-black/30 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4 shadow-xl">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-900">Entrar</h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">
          <X class="h-6 w-6" />
        </button>
      </div>
      
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
          <input v-model="form.email" type="email" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Senha</label>
          <input v-model="form.password" type="password" required class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
        </div>
        
        <div class="flex items-center justify-between">
          <label class="flex items-center">
            <input v-model="form.remember" type="checkbox" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
            <span class="ml-2 text-sm text-gray-600">Lembrar de mim</span>
          </label>
          <a href="#" class="text-sm text-blue-600 hover:text-blue-800">Esqueceu a senha?</a>
        </div>
        
        <button type="submit" class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
          Entrar
        </button>
      </form>
      
      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600">
          Não tem uma conta? 
          <button @click="switchToRegister" class="text-blue-600 hover:text-blue-800 font-medium">
            Cadastre-se
          </button>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { X } from 'lucide-vue-next'

const emit = defineEmits(['close', 'login', 'switch-to-register'])

const form = ref({
  email: '',
  password: '',
  remember: false
})

const handleLogin = () => {
  // Here you would typically validate and send to your backend
  const userData = {
    name: 'João Silva',
    email: form.value.email,
    role: 'student'
  }
  
  emit('login', userData)
}

const switchToRegister = () => {
  emit('close')
  // You could emit a different event to switch modals
}
</script>