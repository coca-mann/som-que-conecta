<template>
  <div class="min-h-screen bg-gradient-to-br from-red-50 via-white to-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="text-center">
        <router-link to="/" class="inline-flex flex-col items-center space-y-3 group">
          <img :src="logoImage" alt="Som que Conecta Logo" class="h-24 w-24 object-contain" />
        </router-link>
        <h2 class="mt-6 text-3xl font-bold text-gray-900">
          Redefina sua Senha
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          Crie uma nova senha segura para sua conta.
        </p>
      </div>

      <div class="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
        <div v-if="successMessage" class="p-4 mb-4 text-center bg-green-100 text-green-800 rounded-lg">
          <p>{{ successMessage }}</p>
          <router-link to="/auth" class="mt-4 inline-block font-bold text-green-900 hover:underline">
            Ir para o Login
          </router-link>
        </div>

        <form v-else class="space-y-6" @submit.prevent="handleResetPassword">
          <p v-if="errorMessage" class="text-center text-sm font-medium text-red-600 bg-red-50 p-3 rounded-lg">
            {{ errorMessage }}
          </p>

          <div>
            <label for="new-password" class="block text-sm font-medium text-gray-700 mb-2">Nova Senha</label>
            <div class="relative">
              <input id="new-password" v-model="form.new_password1" :type="showPassword ? 'text' : 'password'" required placeholder="Digite sua nova senha" class="w-full px-3 py-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent">
              <Lock class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <button type="button" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600" @click="showPassword = !showPassword">
                <component :is="showPassword ? EyeOff : Eye" class="h-5 w-5" />
              </button>
            </div>
          </div>

          <div>
            <label for="confirm-password" class="block text-sm font-medium text-gray-700 mb-2">Confirmar Nova Senha</label>
            <div class="relative">
              <input id="confirm-password" v-model="form.new_password2" :type="showConfirmPassword ? 'text' : 'password'" required placeholder="Confirme sua nova senha" class="w-full px-3 py-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent" :class="{ 'border-red-500': form.new_password2 && !passwordsMatch }">
              <Lock class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            </div>
            <p v-if="form.new_password2 && !passwordsMatch" class="text-xs text-red-600 mt-1">
              As senhas não coincidem.
            </p>
          </div>

          <button type="submit" :disabled="isLoading || !isFormValid" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed">
            <span v-if="!isLoading">Redefinir Senha</span>
            <Loader2 v-else class="h-5 w-5 animate-spin" />
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth.store';
import { Lock, Eye, EyeOff, Loader2 } from 'lucide-vue-next';
import logoImage from '@/assets/logo.png';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

// --- ESTADO DO COMPONENTE ---
const form = ref({
  new_password1: '',
  new_password2: ''
});
const isLoading = ref(false);
const errorMessage = ref(null);
const successMessage = ref(null);
const showPassword = ref(false);
const showConfirmPassword = ref(false);

// --- PROPRIEDADES COMPUTADAS ---
const passwordsMatch = computed(() => form.value.new_password1 === form.value.new_password2);
const isFormValid = computed(() => form.value.new_password1 && passwordsMatch.value);

// --- MÉTODO DE SUBMISSÃO ---
const handleResetPassword = async () => {
  if (!isFormValid.value) return;
  
  isLoading.value = true;
  errorMessage.value = null;

  const payload = {
    uid: route.params.uid,
    token: route.params.token,
    new_password1: form.value.new_password1,
    new_password2: form.value.new_password2,
  };

  try {
    // Chama a action no store para confirmar o reset
    await authStore.confirmPasswordReset(payload);
    successMessage.value = "Senha redefinida com sucesso! Você já pode fazer o login com sua nova senha.";

  } catch (error) {
    const errorData = error.response?.data;
    if (errorData) {
      // Pega os erros da API e os junta em uma única string
      errorMessage.value = Object.values(errorData).flat().join(' ');
    } else {
      errorMessage.value = "O link de recuperação é inválido ou expirou. Por favor, tente novamente.";
    }
    console.error("Erro ao redefinir senha:", error);
  } finally {
    isLoading.value = false;
  }
};
</script>