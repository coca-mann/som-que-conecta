<template>
  <div class="min-h-screen bg-gradient-to-br from-red-50 via-white to-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="text-center">
        <router-link
          to="/"
          class="inline-flex items-center space-x-2 group"
        >
          <Music class="h-10 w-10 text-red-600 transition-transform duration-300 group-hover:scale-110" />
          <span class="text-2xl font-bold text-gray-900">MusicLearn</span>
        </router-link>
        <h2 class="mt-6 text-3xl font-bold text-gray-900">
          {{ isLogin ? 'Bem-vindo de volta!' : 'Crie sua conta' }}
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          {{ isLogin ? 'Entre na sua conta para continuar' : 'Comece sua jornada musical hoje mesmo' }}
        </p>
      </div>

      <div class="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
        <div class="flex bg-gray-100 rounded-lg p-1 mb-8">
          <button
            :class="[
              'flex-1 py-2 px-4 text-sm font-medium rounded-md transition-all duration-300',
              isLogin 
                ? 'bg-white text-red-600 shadow-sm' 
                : 'text-gray-500 hover:text-gray-700'
            ]"
            @click="setMode('login')"
          >
            Entrar
          </button>
          <button
            :class="[
              'flex-1 py-2 px-4 text-sm font-medium rounded-md transition-all duration-300',
              !isLogin 
                ? 'bg-white text-red-600 shadow-sm' 
                : 'text-gray-500 hover:text-gray-700'
            ]"
            @click="setMode('register')"
          >
            Registrar
          </button>
        </div>

        <button
          :disabled="isLoading"
          class="w-full flex items-center justify-center px-4 py-3 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 transition-all duration-300 group disabled:opacity-50 disabled:cursor-not-allowed"
          @click="signInWithGoogle"
        >
          <div class="flex items-center space-x-3">
            <svg
              class="w-5 h-5 transition-transform duration-300 group-hover:scale-110"
              viewBox="0 0 24 24"
            >
              <path
                fill="#4285F4"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="#34A853"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="#FBBC05"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              />
              <path
                fill="#EA4335"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
            </svg>
            <span>{{ isLogin ? 'Entrar' : 'Registrar' }} com Google</span>
          </div>
        </button>

        <div class="relative my-6">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300" />
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500">ou</span>
          </div>
        </div>

        <form
          class="space-y-6"
          @submit.prevent="handleSubmit"
        >
          <Transition
            enter-active-class="transition ease-out duration-300"
            enter-from-class="transform opacity-0 -translate-y-2"
            enter-to-class="transform opacity-100 translate-y-0"
            leave-active-class="transition ease-in duration-200"
            leave-from-class="transform opacity-100 translate-y-0"
            leave-to-class="transform opacity-0 -translate-y-2"
          >
            <div
              v-if="!isLogin"
              class="grid grid-cols-2 gap-4"
            >
              <div>
                <label
                  for="firstName"
                  class="block text-sm font-medium text-gray-700 mb-2"
                >
                  Nome
                </label>
                <input
                  id="firstName"
                  v-model="form.firstName"
                  type="text"
                  required
                  placeholder="João"
                  class="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-300"
                >
              </div>
              <div>
                <label
                  for="lastName"
                  class="block text-sm font-medium text-gray-700 mb-2"
                >
                  Sobrenome
                </label>
                <input
                  id="lastName"
                  v-model="form.lastName"
                  type="text"
                  required
                  placeholder="Silva"
                  class="w-full px-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-300"
                >
              </div>
            </div>
          </Transition>

          <div>
            <label
              for="email"
              class="block text-sm font-medium text-gray-700 mb-2"
            >
              Email
            </label>
            <div class="relative">
              <input
                id="email"
                v-model="form.email"
                type="email"
                required
                placeholder="seu.email@exemplo.com"
                class="w-full px-3 py-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-300"
              >
              <Mail class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            </div>
          </div>

          <div>
            <label
              for="password"
              class="block text-sm font-medium text-gray-700 mb-2"
            >
              Senha
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                :placeholder="isLogin ? 'Sua senha' : 'Mínimo 8 caracteres'"
                class="w-full px-3 py-3 pl-10 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-300"
              >
              <Lock class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <button
                type="button"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
                @click="showPassword = !showPassword"
              >
                <component
                  :is="showPassword ? EyeOff : Eye"
                  class="h-5 w-5"
                />
              </button>
            </div>
            
            <Transition
              enter-active-class="transition ease-out duration-300"
              enter-from-class="transform opacity-0 -translate-y-2"
              enter-to-class="transform opacity-100 translate-y-0"
              leave-active-class="transition ease-in duration-200"
              leave-from-class="transform opacity-100 translate-y-0"
              leave-to-class="transform opacity-0 -translate-y-2"
            >
              <div
                v-if="!isLogin && form.password"
                class="mt-2"
              >
                <div class="flex space-x-1">
                  <div
                    v-for="i in 4"
                    :key="i"
                    :class="[
                      'h-1 flex-1 rounded-full transition-all duration-300',
                      i <= passwordStrength.score
                        ? passwordStrength.color
                        : 'bg-gray-200'
                    ]"
                  />
                </div>
                <p :class="['text-xs mt-1', passwordStrength.textColor]">
                  {{ passwordStrength.text }}
                </p>
              </div>
            </Transition>
          </div>

          <Transition
            enter-active-class="transition ease-out duration-300"
            enter-from-class="transform opacity-0 -translate-y-2"
            enter-to-class="transform opacity-100 translate-y-0"
            leave-active-class="transition ease-in duration-200"
            leave-from-class="transform opacity-100 translate-y-0"
            leave-to-class="transform opacity-0 -translate-y-2"
          >
            <div v-if="!isLogin">
              <label
                for="confirmPassword"
                class="block text-sm font-medium text-gray-700 mb-2"
              >
                Confirmar Senha
              </label>
              <div class="relative">
                <input
                  id="confirmPassword"
                  v-model="form.confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  required
                  placeholder="Confirme sua senha"
                  class="w-full px-3 py-3 pl-10 pr-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent transition-all duration-300"
                  :class="{ 'border-red-300': form.confirmPassword && !passwordsMatch }"
                >
                <Lock class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                <button
                  type="button"
                  class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors duration-200"
                  @click="showConfirmPassword = !showConfirmPassword"
                >
                  <component
                    :is="showConfirmPassword ? EyeOff : Eye"
                    class="h-5 w-5"
                  />
                </button>
              </div>
              <p
                v-if="form.confirmPassword && !passwordsMatch"
                class="text-xs text-red-600 mt-1"
              >
                As senhas não coincidem
              </p>
            </div>
          </Transition>

          <Transition
            enter-active-class="transition ease-out duration-300"
            enter-from-class="transform opacity-0 -translate-y-2"
            enter-to-class="transform opacity-100 translate-y-0"
            leave-active-class="transition ease-in duration-200"
            leave-from-class="transform opacity-100 translate-y-0"
            leave-to-class="transform opacity-0 -translate-y-2"
          >
            <div
              v-if="!isLogin"
              class="flex items-start space-x-2"
            >
              <input
                id="terms"
                v-model="form.acceptTerms"
                type="checkbox"
                required
                class="mt-1 h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300 rounded transition-colors duration-200"
              >
              <label
                for="terms"
                class="text-sm text-gray-600"
              >
                Eu concordo com os 
                <router-link
                  to="/terms"
                  class="text-red-600 hover:text-red-700 underline"
                >
                  Termos de Uso
                </router-link>
                e a
                <router-link
                  to="/privacy"
                  class="text-red-600 hover:text-red-700 underline"
                >
                  Política de Privacidade
                </router-link>
              </label>
            </div>
          </Transition>

          <Transition
            enter-active-class="transition ease-out duration-300"
            enter-from-class="transform opacity-0 -translate-y-2"
            enter-to-class="transform opacity-100 translate-y-0"
            leave-active-class="transition ease-in duration-200"
            leave-from-class="transform opacity-100 translate-y-0"
            leave-to-class="transform opacity-0 -translate-y-2"
          >
            <div>
              <div
                v-if="isLogin"
                class="flex items-center justify-between"
              >
                <div class="flex items-center">
                  <input
                    id="remember"
                    v-model="form.rememberMe"
                    type="checkbox"
                    class="h-4 w-4 text-red-600 focus:ring-red-500 border-gray-300 rounded transition-colors duration-200"
                  >
                  <label
                    for="remember"
                    class="ml-2 text-sm text-gray-600"
                  >
                    Lembrar de mim
                  </label>
                </div>
                <button
                  type="button"
                  class="text-sm text-red-600 hover:text-red-700 transition-colors duration-200"
                  @click="showForgotPassword = true"
                >
                  Esqueceu a senha?
                </button>
              </div>
              <p
                v-if="errorMessage"
                class="text-center text-sm font-medium text-red-600 bg-red-50 p-3 rounded-lg"
              >
                {{ errorMessage }}
              </p>
            </div>
          </Transition>

          <button
            type="submit"
            :disabled="isLoading || (!isLogin && !isFormValid)"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 group"
          >
            <span
              v-if="!isLoading"
              class="flex items-center space-x-2"
            >
              <span>{{ isLogin ? 'Entrar' : 'Criar Conta' }}</span>
              <ArrowRight class="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
            </span>
            <div
              v-else
              class="flex items-center space-x-2"
            >
              <Loader2 class="h-4 w-4 animate-spin" />
              <span>{{ isLogin ? 'Entrando...' : 'Criando conta...' }}</span>
            </div>
          </button>
        </form>

        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            {{ isLogin ? 'Não tem uma conta?' : 'Já tem uma conta?' }}
            <button
              class="font-medium text-red-600 hover:text-red-700 transition-colors duration-200"
              @click="toggleMode"
            >
              {{ isLogin ? 'Registre-se aqui' : 'Entre aqui' }}
            </button>
          </p>
        </div>
      </div>

      <div class="grid grid-cols-3 gap-4 mt-8">
        <div class="text-center">
          <div class="inline-flex items-center justify-center w-10 h-10 bg-red-100 rounded-lg mb-2">
            <BookOpen class="h-5 w-5 text-red-600" />
          </div>
          <p class="text-xs text-gray-600">
            Cursos Online
          </p>
        </div>
        <div class="text-center">
          <div class="inline-flex items-center justify-center w-10 h-10 bg-gray-200 rounded-lg mb-2">
            <Users class="h-5 w-5 text-gray-600" />
          </div>
          <p class="text-xs text-gray-600">
            Comunidade
          </p>
        </div>
        <div class="text-center">
          <div class="inline-flex items-center justify-center w-10 h-10 bg-red-100 rounded-lg mb-2">
            <Newspaper class="h-5 w-5 text-red-600" />
          </div>
          <p class="text-xs text-gray-600">
            Artigos
          </p>
        </div>
      </div>
    </div>

    <Transition
      enter-active-class="transition ease-out duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="showForgotPassword"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
      >
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-semibold text-gray-900">
              Recuperar Senha
            </h3>
            <button
              class="text-gray-400 hover:text-red-600 transition-colors duration-200"
              @click="showForgotPassword = false"
            >
              <X class="h-6 w-6" />
            </button>
          </div>
          
          <p class="text-sm text-gray-600 mb-4">
            Digite seu email e enviaremos um link para redefinir sua senha.
          </p>
          
          <form
            class="space-y-4"
            @submit.prevent="handleForgotPassword"
          >
            <div>
              <label
                for="resetEmail"
                class="block text-sm font-medium text-gray-700 mb-2"
              >
                Email
              </label>
              <input
                id="resetEmail"
                v-model="resetEmail"
                type="email"
                required
                placeholder="seu.email@exemplo.com"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              >
            </div>
            
            <div class="flex space-x-3">
              <button
                type="button"
                class="flex-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors duration-200"
                @click="showForgotPassword = false"
              >
                Cancelar
              </button>
              <button
                type="submit"
                :disabled="isLoading"
                class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 transition-colors duration-200"
              >
                Enviar Link
              </button>
            </div>
          </form>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth.store';
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  Music,
  Mail,
  Lock,
  Eye,
  EyeOff,
  ArrowRight,
  Loader2,
  X,
  BookOpen,
  Users,
  Award,
  newspaper,
  Newspaper
} from 'lucide-vue-next'

const errorMessage = ref(null);

const router = useRouter()
const route = useRoute()

// State
const isLogin = ref(true)
const isLoading = ref(false)
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const showForgotPassword = ref(false)
const resetEmail = ref('')
const authStore = useAuthStore();

// Form data
const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
  rememberMe: false,
  acceptTerms: false
})

// Computed properties
const passwordsMatch = computed(() => {
  return form.value.password === form.value.confirmPassword
})

const passwordStrength = computed(() => {
  const password = form.value.password
  let score = 0
  
  if (password.length >= 8) score++
  if (/[a-z]/.test(password)) score++
  if (/[A-Z]/.test(password)) score++
  if (/[0-9]/.test(password)) score++
  if (/[^A-Za-z0-9]/.test(password)) score++
  
  const levels = [
    { score: 0, text: 'Muito fraca', color: 'bg-red-500', textColor: 'text-red-600' },
    { score: 1, text: 'Fraca', color: 'bg-red-400', textColor: 'text-red-600' },
    { score: 2, text: 'Regular', color: 'bg-yellow-400', textColor: 'text-yellow-600' },
    { score: 3, text: 'Boa', color: 'bg-blue-400', textColor: 'text-blue-600' },
    { score: 4, text: 'Forte', color: 'bg-green-500', textColor: 'text-green-600' }
  ]
  
  return { ...levels[Math.min(score, 4)], score }
})

const isFormValid = computed(() => {
  if (isLogin.value) {
    return form.value.email && form.value.password
  } else {
    return (
      form.value.firstName &&
      form.value.lastName &&
      form.value.email &&
      form.value.password &&
      form.value.confirmPassword &&
      passwordsMatch.value &&
      form.value.acceptTerms &&
      passwordStrength.value.score >= 2
    )
  }
})

// Methods
const setMode = (mode) => {
  isLogin.value = mode === 'login'
  clearForm()
}

const toggleMode = () => {
  isLogin.value = !isLogin.value
  clearForm()
}

const clearForm = () => {
  form.value = {
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    rememberMe: false,
    acceptTerms: false
  }
}

const handleSubmit = async () => {
  console.log("A. Função handleSubmit foi ACIONADA.");
  console.log("B. O valor de isLogin.value é:", isLogin.value);
  console.log("C. O valor de isFormValid.value é:", isFormValid.value);

  errorMessage.value = null; 
  if (!isFormValid.value) {
    console.log("Formulário inválido, execução parada.");
    return;
  }
  
  isLoading.value = true;
  
  try {
    // Lógica de Login (continua a mesma)
    if (isLogin.value) {
      await authStore.login({
        email: form.value.email,
        password: form.value.password,
      });

      // Usa o parâmetro redirect da URL ou redireciona para a home
      const redirectTo = route.query.redirect || '/';
      router.push(redirectTo);
    } else {
      await authStore.register({
        email: form.value.email,
        password: form.value.password,
        first_name: form.value.firstName,
        last_name: form.value.lastName,
      });
      // 2. Se o registro for bem-sucedido:
      alert('Conta criada com sucesso! Por favor, faça o login para continuar.');
      router.push('/');
    }
    
  } catch (error) {
    console.error("F. ERRO CAPTURADO no handleSubmit:", error);
    if (error.response && error.response.data) {
        const errorData = error.response.data;
        let errorMessages = [];
        for (const field in errorData) {
            errorMessages.push(`${field}: ${errorData[field].join(', ')}`);
        }
        errorMessage.value = errorMessages.join(' | ');
    } else {
        errorMessage.value = 'Não foi possível conectar ao servidor. Verifique sua conexão.';
    }
  } finally {
    isLoading.value = false;
  }
}

const signInWithGoogle = async () => {
  isLoading.value = true
  
  try {
    // Simulate Google OAuth
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    console.log('Google sign in')
    
    // In a real app, you would integrate with Google OAuth
    // Example: const result = await signInWithPopup(auth, googleProvider)
    
    const redirectTo = route.query.redirect || '/'
    router.push(redirectTo)
    
  } catch (error) {
    console.error('Google sign in error:', error)
  } finally {
    isLoading.value = false
  }
}

const handleForgotPassword = async () => {
  if (!resetEmail.value) return
  
  isLoading.value = true
  
  try {
    // Simulate password reset
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    console.log('Password reset for:', resetEmail.value)
    alert('Link de recuperação enviado para seu email!')
    
    showForgotPassword.value = false
    resetEmail.value = ''
    
  } catch (error) {
    console.error('Password reset error:', error)
  } finally {
    isLoading.value = false
  }
}

// Initialize based on route query
const initializeMode = () => {
  if (route.query.mode === 'register') {
    isLogin.value = false
  }
}

onMounted(() => {
  initializeMode()
})

// Watch for route changes
watch(() => route.query.mode, (newMode) => {
  if (newMode === 'register') {
    isLogin.value = false
  } else if (newMode === 'login') {
    isLogin.value = true
  }
})
</script>

<style scoped>
/* Custom focus styles */
input:focus {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Smooth transitions for all interactive elements */
* {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Custom checkbox styles */
input[type="checkbox"]:checked {
  background-image: url("data:image/svg+xml,%3csvg viewBox='0 0 16 16' fill='white' xmlns='http://www.w3.org/2000/svg'%3e%3cpath d='m13.854 3.646-7.5 7.5a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6 10.293l7.146-7.147a.5.5 0 0 1 .708.708z'/%3e%3c/svg%3e");
}

/* Gradient background animation */
.bg-gradient-to-br {
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
</style> 