<template>
  <div class="min-h-screen bg-gray-100 flex flex-col justify-center items-center p-4">
    <div class="max-w-md w-full bg-white rounded-2xl shadow-xl p-8 text-center">
      
      <div v-if="isLoading" class="flex justify-center items-center flex-col">
        <Loader2 class="h-12 w-12 text-red-600 animate-spin" />
        <h2 class="mt-4 text-2xl font-bold text-gray-800">{{ message }}</h2>
      </div>

      <div v-if="isSuccess" class="flex justify-center items-center flex-col">
        <CircleCheck class="h-12 w-12 text-green-500" />
        <h2 class="mt-4 text-2xl font-bold text-gray-800">Sucesso!</h2>
        <p class="mt-2 text-gray-600">{{ message }}</p>
        <router-link
          to="/auth"
          class="mt-6 inline-block w-full px-4 py-3 bg-red-600 text-white font-medium rounded-lg hover:bg-red-700 transition-colors duration-300"
        >
          Ir para o Login
        </router-link>
      </div>
      
      <div v-if="isError" class="flex justify-center items-center flex-col">
        <CircleX class="h-12 w-12 text-red-500" />
        <h2 class="mt-4 text-2xl font-bold text-gray-800">Ocorreu um Erro</h2>
        <p class="mt-2 text-gray-600">{{ message }}</p>
        <router-link
          to="/auth?mode=register"
          class="mt-6 inline-block w-full px-4 py-3 bg-gray-600 text-white font-medium rounded-lg hover:bg-gray-700 transition-colors duration-300"
        >
          Tentar se registrar novamente
        </router-link>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios'; // Ou seu serviço de API
import { Loader2, CircleCheck, CircleX } from 'lucide-vue-next';

// Estado do componente
const isLoading = ref(true);
const isSuccess = ref(false);
const isError = ref(false);
const message = ref('Ativando sua conta, por favor aguarde...');

// Hook para acessar a rota atual
const route = useRoute();

// Função que é executada assim que o componente é montado na tela
onMounted(async () => {
  // 1. Pega o token da URL (o nome 'token' deve ser o mesmo do parâmetro na rota)
  const token = route.params.token;

  if (!token) {
    message.value = 'Nenhum token de ativação fornecido.';
    isError.value = true;
    isLoading.value = false;
    return;
  }

  try {
    // 2. Faz a chamada GET para a API de ativação do Django
    //    Certifique-se de que a URL base da sua API está correta
    const response = await axios.get(`${process.env.VUE_APP_BASE_URL}/api/activate/${token}/`);

    // 3. Processa a resposta de sucesso
    message.value = response.data.message;
    isSuccess.value = true;

  } catch (error) {
    // 4. Processa a resposta de erro
    if (error.response && error.response.data && error.response.data.error) {
      message.value = error.response.data.error;
    } else {
      message.value = 'Não foi possível conectar ao servidor para ativar a conta.';
    }
    isError.value = true;
    
  } finally {
    // 5. Esconde o indicador de carregamento
    isLoading.value = false;
  }
});
</script>