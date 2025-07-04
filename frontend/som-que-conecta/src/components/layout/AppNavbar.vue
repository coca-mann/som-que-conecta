<template>
  <nav class="bg-white/95 backdrop-blur-md shadow-lg sticky top-0 z-50 border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <router-link
            to="/"
            class="flex items-center space-x-2 group"
          >
            <div class="relative">
              <img 
                :src="logoImage" 
                alt="Som que Conecta Logo"
                class="h-10 w-10 text-red-600 transition-all duration-300 group-hover:scale-110 group-hover:rotate-12 object-contain"
              >
              <div class="absolute inset-0 bg-red-600/20 rounded-full scale-0 group-hover:scale-150 transition-transform duration-300" />
            </div>
            <span class="text-xl font-bold text-gray-900 transition-colors duration-300 group-hover:text-red-600">
              Som que Conecta
            </span>
          </router-link>
        </div>
        
        <div class="hidden md:flex items-center space-x-2">
          <router-link 
            v-for="link in navigationLinks" 
            :key="link.path"
            :to="link.path" 
            class="relative px-4 py-2 text-gray-700 hover:text-red-600 rounded-lg transition-all duration-300 group overflow-hidden"
            :class="{ 'text-red-600 bg-red-50 font-medium': isActiveRoute(link.path) }"
          >
            <div class="absolute inset-0 bg-gradient-to-r from-red-50 to-red-100 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left rounded-lg" />
            <span class="relative z-10 flex items-center space-x-2">
              <component
                :is="link.icon"
                class="h-4 w-4 transition-transform duration-300 group-hover:scale-110"
              />
              <span>{{ link.name }}</span>
            </span>
            <div 
              v-if="isActiveRoute(link.path)"
              class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-6 h-0.5 bg-red-600 rounded-full"
            />
          </router-link>
        </div>

        <div class="flex items-center space-x-4">
          <div
            v-if="authStore.isAuthenticated"
            class="relative user-menu"
          >
            <button 
              class="flex items-center space-x-2 text-gray-700 hover:text-red-600 p-2 rounded-lg transition-all duration-300 group"
              @click="toggleUserMenu"
            >
              <div class="relative">
                <img 
                  :src="profilePictureUrl" 
                  :alt="userName"
                  class="h-8 w-8 rounded-full border-2 border-transparent group-hover:border-red-200 transition-all duration-300"
                >
                <div class="absolute inset-0 rounded-full bg-red-600/10 scale-0 group-hover:scale-100 transition-transform duration-300" />
              </div>
              <span class="hidden sm:block font-medium">{{ userName }}</span>
              <ChevronDown 
                class="h-4 w-4 transition-all duration-300"
                :class="{ 'rotate-180': showUserMenu }"
              />
            </button>
            
            <Transition
              enter-active-class="transition ease-out duration-200"
              enter-from-class="transform opacity-0 scale-95 translate-y-2"
              enter-to-class="transform opacity-100 scale-100 translate-y-0"
              leave-active-class="transition ease-in duration-150"
              leave-from-class="transform opacity-100 scale-100 translate-y-0"
              leave-to-class="transform opacity-0 scale-95 translate-y-2"
            >
              <div
                v-if="showUserMenu"
                class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-gray-200 py-2 z-50 overflow-hidden user-menu"
              >
                <div class="px-4 py-3 border-b border-gray-200">
                  <div class="flex items-center space-x-3">
                    <img 
                      :src="profilePictureUrl" 
                      :alt="userName"
                      class="h-10 w-10 rounded-full"
                    >
                    <div>
                      <p class="text-sm font-medium text-gray-900">
                        {{ userName }}
                      </p>
                      <p class="text-xs text-gray-500">
                        {{ authStore.user?.email }}
                      </p>
                    </div>
                  </div>
                </div>

                <div class="py-1">
                  <router-link 
                    v-for="item in userMenuItems" 
                    :key="item.path" 
                    :to="item.path" 
                    class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-red-600 transition-all duration-200 group"
                    @click="closeUserMenu"
                  >
                    <component
                      :is="item.icon"
                      class="h-4 w-4 mr-3 transition-transform duration-200 group-hover:scale-110"
                    />
                    {{ item.name }}
                  </router-link>
                  
                  <div class="border-t border-gray-200 my-1" />
                  
                  <button 
                    class="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-all duration-200 group" 
                    @click="() => { handleLogout(); closeUserMenu(); }"
                  >
                    <LogOut class="h-4 w-4 mr-3 transition-transform duration-200 group-hover:scale-110" />
                    Sair
                  </button>
                </div>
              </div>
            </Transition>
          </div>

          <div
            v-if="!authStore.isAuthenticated"
            class="flex items-center space-x-2"
          >
            <router-link
              to="/auth?mode=login"
              class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-red-600 transition-colors duration-200"
            >
              Entrar
            </router-link>
            <router-link
              to="/auth?mode=register"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors duration-200"
            >
              Cadastrar
            </router-link>
          </div>
          
          <button
            id="hamburger-menu-btn"
            class="md:hidden p-2 text-gray-700 hover:text-red-600 hover:bg-red-50 rounded-lg transition-all duration-300"
            @click="toggleMobileMenu"
          >
            <div class="relative w-6 h-6">
              <span
                class="absolute block h-0.5 w-6 bg-current transform transition-all duration-300"
                :class="showMobileMenu ? 'rotate-45 translate-y-2.5' : 'translate-y-1'"
              />
              <span
                class="absolute block h-0.5 w-6 bg-current transform transition-all duration-300"
                :class="showMobileMenu ? 'opacity-0' : 'translate-y-2.5'"
              />
              <span
                class="absolute block h-0.5 w-6 bg-current transform transition-all duration-300"
                :class="showMobileMenu ? '-rotate-45 translate-y-2.5' : 'translate-y-4'"
              />
            </div>
          </button>
        </div>
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
          v-if="showSearch"
          class="border-t border-gray-200 py-4"
        />
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
          v-if="showMobileMenu"
          class="md:hidden border-t border-gray-200 bg-white py-4 space-y-2 mobile-menu"
        >
          <router-link
            v-for="link in navigationLinks"
            :key="link.path"
            :to="link.path"
            class="block px-4 py-2 text-gray-700 hover:text-red-600 rounded-lg transition-all duration-300"
            @click="showMobileMenu = false"
          >
            <span class="flex items-center gap-2">
              <component :is="link.icon" class="h-4 w-4" />
              {{ link.name }}
            </span>
          </router-link>
          <div v-if="authStore.isAuthenticated" class="border-t border-gray-100 my-2" />
          <div v-if="authStore.isAuthenticated" class="px-4">
            <router-link to="/profile" class="block py-2 text-gray-700 hover:text-red-600">Meu Perfil</router-link>
            <button
              class="block w-full text-left py-2 text-red-600 hover:bg-red-50 rounded-lg"
              @click="() => { handleLogout(); showMobileMenu = false; }"
            >Sair</button>
          </div>
          <div v-else class="px-4">
            <router-link to="/auth?mode=login" class="block py-2 text-gray-700 hover:text-red-600">Entrar</router-link>
            <router-link to="/auth?mode=register" class="block py-2 text-white bg-red-600 hover:bg-red-700 rounded-lg text-center">Cadastrar</router-link>
          </div>
        </div>
      </Transition>
    </div>
  </nav>
</template>

<script setup>
console.log("Executando setup de AppNavbar.vue");
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
// A importação do store
import { useAuthStore } from '@/stores/auth.store';
import logoImage from '@/assets/logo.png';

import { 
  Music, User, ChevronDown, LogOut, Search, X, Home, FileText,
  Guitar, BookOpen, Settings, HelpCircle, Calendar
} from 'lucide-vue-next'

// 2. CRIAMOS A INSTÂNCIA DO STORE PARA USAR NO COMPONENTE
const authStore = useAuthStore();
const router = useRouter();
const route = useRoute()
const searchInput = ref(null)

// State local do componente (apenas para controle da UI)
const showMobileMenu = ref(false)
const showUserMenu = ref(false)
const showSearch = ref(false)
const searchQuery = ref('')

// 3. REMOVEMOS O ESTADO LOCAL 'isLoggedIn' e 'user'. Usaremos o store.

// 4. LÓGICA DE NOTIFICAÇÕES REMOVIDA

// Navigation links
const navigationLinks = [
  { name: 'Início', path: '/', icon: Home },
  { name: 'Artigos', path: '/articles', icon: FileText },
  { name: 'Instrumentos', path: '/instruments', icon: Guitar },
  { name: 'Minicursos', path: '/courses', icon: BookOpen }
]

// Propriedade computada para exibir o nome do usuário
const userName = computed(() => {
  // O '?' (optional chaining) evita erros se o usuário for nulo
  return authStore.user?.first_name || 'Usuário'; 
})

// Propriedade computada para a URL da imagem de perfil
const profilePictureUrl = computed(() => {
  // Usa a variável de ambiente definida em .env na raiz do frontend
  const baseUrl = process.env.VUE_APP_BASE_URL || '';
  if (authStore.user?.profile_picture) {
    return `${baseUrl}${authStore.user.profile_picture}`;
  }
  return '/placeholder.svg?height=32&width=32';
})

const handleLogout = () => {
  authStore.logout(); // Chama a ação para limpar o estado
  router.push('/auth'); // Faz o redirect aqui no componente
}

// User menu items
const userMenuItems = computed(() => {
  const items = [
    { name: 'Meu Perfil', path: '/profile', icon: User },
    { name: 'Gerenciar Instrumentos', path: '/manage-instruments', icon: Guitar }
  ]
  
  // Adiciona o item de agendamentos apenas para roles específicos
  if (authStore.user?.role && ['admin', 'ong', 'professor'].includes(authStore.user.role)) {
    items.push({ name: 'Gerenciar Agendamentos', path: '/bookings', icon: Calendar })
  }
  
  // Adiciona o item de ajuda por último
  items.push({ name: 'Ajuda', path: '/help', icon: HelpCircle })
  
  return items
})

// O restante dos seus métodos de UI continua o mesmo
const isActiveRoute = (path) => {
  if (path === '/') {
    return route.path === '/'
  }
  if (path === '/courses') {
    return route.path === '/courses' || route.path.startsWith('/courses/') || route.path.startsWith('/course/')
  }
  return route.path.startsWith(path)
}

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
  if (showMobileMenu.value) {
    showUserMenu.value = false
    showSearch.value = false
  }
}
const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
  if (showUserMenu.value) {
    showMobileMenu.value = false
    showSearch.value = false
  }
}

// 5. A FUNÇÃO DE LOGOUT FOI REMOVIDA. Usaremos a do store diretamente no template.

const closeMenus = (event) => {
  // Fecha o menu do usuário se o clique foi fora dele
  if (showUserMenu.value && !event.target.closest('.user-menu')) {
    showUserMenu.value = false
  }
  // Fecha o menu mobile se o clique foi fora dele e fora do botão do menu
  if (
    showMobileMenu.value &&
    !event.target.closest('.mobile-menu') &&
    !event.target.closest('#hamburger-menu-btn')
  ) {
    showMobileMenu.value = false
  }
  // Fecha a busca se o clique foi fora dela
  if (showSearch.value && !event.target.closest('.search-container')) {
    showSearch.value = false
  }
}

const closeUserMenu = () => {
  showUserMenu.value = false
}

// Event listeners
onMounted(() => {
  document.addEventListener('click', closeMenus)
})

onUnmounted(() => {
  document.removeEventListener('click', closeMenus)
})

// Watchers
watch(() => route.path, () => { /* ... */ })
watch(searchQuery, (newQuery) => { /* ... */ })
</script>

<style scoped>
/* Estilos continuam os mesmos */
</style>