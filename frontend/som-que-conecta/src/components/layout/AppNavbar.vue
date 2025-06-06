<template>
  <nav class="bg-white/95 backdrop-blur-md shadow-lg sticky top-0 z-50 border-b border-gray-100">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link 
            to="/" 
            class="flex items-center space-x-2 group"
          >
            <div class="relative">
              <Music class="h-8 w-8 text-blue-600 transition-all duration-300 group-hover:scale-110 group-hover:rotate-12" />
              <div class="absolute inset-0 bg-blue-600/20 rounded-full scale-0 group-hover:scale-150 transition-transform duration-300"></div>
            </div>
            <span class="text-xl font-bold text-gray-900 transition-colors duration-300 group-hover:text-blue-600">
              MusicLearn
            </span>
          </router-link>
        </div>
        
        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-2">
          <router-link 
            v-for="link in navigationLinks" 
            :key="link.path"
            :to="link.path" 
            class="relative px-4 py-2 text-gray-700 hover:text-blue-600 rounded-lg transition-all duration-300 group overflow-hidden"
            :class="{ 'text-blue-600 bg-blue-50 font-medium': isActiveRoute(link.path) }"
          >
            <!-- Background animation -->
            <div class="absolute inset-0 bg-gradient-to-r from-blue-50 to-blue-100 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300 origin-left rounded-lg"></div>
            
            <!-- Text -->
            <span class="relative z-10 flex items-center space-x-2">
              <component :is="link.icon" class="h-4 w-4 transition-transform duration-300 group-hover:scale-110" />
              <span>{{ link.name }}</span>
            </span>
            
            <!-- Active indicator -->
            <div 
              v-if="isActiveRoute(link.path)"
              class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-6 h-0.5 bg-blue-600 rounded-full"
            ></div>
          </router-link>
        </div>

        <!-- Right side actions -->
        <div class="flex items-center space-x-4">
          <!-- Search Button -->
          <button 
            @click="toggleSearch"
            class="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-300 group"
          >
            <Search class="h-5 w-5 transition-transform duration-300 group-hover:scale-110" />
          </button>

          <!-- Notifications (only when logged in) -->
          <div v-if="isLoggedIn" class="relative">
            <button 
              @click="toggleNotifications"
              class="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-300 group relative"
            >
              <Bell class="h-5 w-5 transition-transform duration-300 group-hover:scale-110" />
              <div 
                v-if="hasNotifications"
                class="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-pulse"
              ></div>
            </button>
            
            <!-- Notifications Dropdown -->
            <Transition
              enter-active-class="transition ease-out duration-200"
              enter-from-class="transform opacity-0 scale-95 translate-y-2"
              enter-to-class="transform opacity-100 scale-100 translate-y-0"
              leave-active-class="transition ease-in duration-150"
              leave-from-class="transform opacity-100 scale-100 translate-y-0"
              leave-to-class="transform opacity-0 scale-95 translate-y-2"
            >
              <div 
                v-if="showNotifications" 
                class="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-xl border border-gray-100 py-2 z-50 overflow-hidden"
              >
                <div class="px-4 py-3 border-b border-gray-100">
                  <h3 class="text-sm font-semibold text-gray-900">Notificações</h3>
                </div>
                <div class="max-h-64 overflow-y-auto">
                  <div v-for="notification in notifications" :key="notification.id" class="px-4 py-3 hover:bg-gray-50 transition-colors duration-200">
                    <div class="flex items-start space-x-3">
                      <div class="flex-shrink-0">
                        <div class="w-2 h-2 bg-blue-500 rounded-full mt-2"></div>
                      </div>
                      <div class="flex-1 min-w-0">
                        <p class="text-sm text-gray-900">{{ notification.message }}</p>
                        <p class="text-xs text-gray-500 mt-1">{{ notification.time }}</p>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="px-4 py-2 border-t border-gray-100">
                  <button class="text-sm text-blue-600 hover:text-blue-700 font-medium">Ver todas</button>
                </div>
              </div>
            </Transition>
          </div>

          <!-- User Menu (only when logged in) -->
          <div v-if="isLoggedIn" class="relative">
            <button 
              class="flex items-center space-x-2 text-gray-700 hover:text-blue-600 p-2 rounded-lg transition-all duration-300 group"
              @click="toggleUserMenu"
            >
              <div class="relative">
                <img 
                  :src="user.avatar || '/placeholder.svg?height=32&width=32'" 
                  :alt="user.name"
                  class="h-8 w-8 rounded-full border-2 border-transparent group-hover:border-blue-200 transition-all duration-300"
                />
                <div class="absolute inset-0 rounded-full bg-blue-600/10 scale-0 group-hover:scale-100 transition-transform duration-300"></div>
              </div>
              <span class="hidden sm:block font-medium">{{ user.name }}</span>
              <ChevronDown 
                class="h-4 w-4 transition-all duration-300"
                :class="{ 'rotate-180': showUserMenu }"
              />
            </button>
            
            <!-- User Dropdown -->
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
                class="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-gray-100 py-2 z-50 overflow-hidden"
              >
                <!-- User Info -->
                <div class="px-4 py-3 border-b border-gray-100">
                  <div class="flex items-center space-x-3">
                    <img 
                      :src="user.avatar || '/placeholder.svg?height=40&width=40'" 
                      :alt="user.name"
                      class="h-10 w-10 rounded-full"
                    />
                    <div>
                      <p class="text-sm font-medium text-gray-900">{{ user.name }}</p>
                      <p class="text-xs text-gray-500">{{ user.email }}</p>
                    </div>
                  </div>
                </div>

                <!-- Menu Items -->
                <div class="py-1">
                  <router-link 
                    v-for="item in userMenuItems"
                    :key="item.path"
                    :to="item.path" 
                    class="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-blue-600 transition-all duration-200 group"
                  >
                    <component :is="item.icon" class="h-4 w-4 mr-3 transition-transform duration-200 group-hover:scale-110" />
                    {{ item.name }}
                  </router-link>
                  
                  <div class="border-t border-gray-100 my-1"></div>
                  
                  <button 
                    class="flex items-center w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-all duration-200 group"
                    @click="logout"
                  >
                    <LogOut class="h-4 w-4 mr-3 transition-transform duration-200 group-hover:scale-110" />
                    Sair
                  </button>
                </div>
              </div>
            </Transition>
          </div>

          <!-- Auth Buttons (only when logged out) -->
          <div v-if="!isLoggedIn" class="flex items-center space-x-2">
            <router-link 
              to="/auth?mode=login"
              class="px-4 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors duration-200"
            >
              Entrar
            </router-link>
            <router-link 
              to="/auth?mode=register"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors duration-200"
            >
              Cadastrar
            </router-link>
          </div>
          
          <!-- Mobile menu button -->
          <button 
            class="md:hidden p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-300"
            @click="toggleMobileMenu"
          >
            <div class="relative w-6 h-6">
              <span 
                class="absolute block h-0.5 w-6 bg-current transform transition-all duration-300"
                :class="showMobileMenu ? 'rotate-45 translate-y-2.5' : 'translate-y-1'"
              ></span>
              <span 
                class="absolute block h-0.5 w-6 bg-current transform transition-all duration-300"
                :class="showMobileMenu ? 'opacity-0' : 'translate-y-2.5'"
              ></span>
              <span 
                class="absolute block h-0.5 w-6 bg-current transform transition-all duration-300"
                :class="showMobileMenu ? '-rotate-45 translate-y-2.5' : 'translate-y-4'"
              ></span>
            </div>
          </button>
        </div>
      </div>
      
      <!-- Search Bar -->
      <Transition
        enter-active-class="transition ease-out duration-300"
        enter-from-class="transform opacity-0 -translate-y-2"
        enter-to-class="transform opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="transform opacity-100 translate-y-0"
        leave-to-class="transform opacity-0 -translate-y-2"
      >
        <div v-if="showSearch" class="border-t border-gray-100 py-4">
          <div class="relative max-w-md mx-auto">
            <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input 
              ref="searchInput"
              v-model="searchQuery"
              type="text" 
              placeholder="Buscar cursos, artigos, instrumentos..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300"
              @keydown.escape="closeSearch"
            />
            <button 
              @click="closeSearch"
              class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              <X class="h-5 w-5" />
            </button>
          </div>
        </div>
      </Transition>
      
      <!-- Mobile menu -->
      <Transition
        enter-active-class="transition ease-out duration-300"
        enter-from-class="transform opacity-0 -translate-y-2"
        enter-to-class="transform opacity-100 translate-y-0"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="transform opacity-100 translate-y-0"
        leave-to-class="transform opacity-0 -translate-y-2"
      >
        <div v-if="showMobileMenu" class="md:hidden border-t border-gray-100">
          <div class="px-2 pt-2 pb-3 space-y-1">
            <router-link 
              v-for="link in navigationLinks"
              :key="link.path"
              :to="link.path" 
              class="flex items-center space-x-3 px-3 py-3 text-gray-700 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all duration-300 group"
              :class="{ 'text-blue-600 bg-blue-50 font-medium': isActiveRoute(link.path) }"
            >
              <component :is="link.icon" class="h-5 w-5 transition-transform duration-300 group-hover:scale-110" />
              <span>{{ link.name }}</span>
            </router-link>
          </div>
        </div>
      </Transition>
    </div>
    
    
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { 
  Music, 
  User, 
  ChevronDown, 
  Menu, 
  LogOut, 
  Search, 
  Bell, 
  X,
  Home,
  FileText,
  Guitar,
  BookOpen,
  Settings,
  HelpCircle
} from 'lucide-vue-next'


const router = useRouter()
const route = useRoute()
const searchInput = ref(null)

// State
const showMobileMenu = ref(false)
const showUserMenu = ref(false)
const showSearch = ref(false)
const showNotifications = ref(false)
const searchQuery = ref('')

// User data
const user = ref({
  name: 'João Silva',
  email: 'joao.silva@email.com',
  avatar: '/placeholder.svg?height=32&width=32',
  role: 'teacher'
})

const isLoggedIn = ref(true)
const hasNotifications = ref(true)

// Navigation links
const navigationLinks = [
  { name: 'Início', path: '/', icon: Home },
  { name: 'Artigos', path: '/articles', icon: FileText },
  { name: 'Instrumentos', path: '/instruments', icon: Guitar },
  { name: 'Minicursos', path: '/courses', icon: BookOpen }
]

// User menu items
const userMenuItems = computed(() => {
  const items = [
    { name: 'Meu Perfil', path: '/profile', icon: User },
    { name: 'Configurações', path: '/settings', icon: Settings },
    { name: 'Ajuda', path: '/help-center', icon: HelpCircle }
  ]
  
  if (isTeacherOrAdmin.value) {
    items.splice(1, 0, { name: 'Gerenciar Instrumentos', path: '/manage-instruments', icon: Guitar })
  }
  
  return items
})

// Sample notifications
const notifications = ref([
  {
    id: 1,
    message: 'Novo curso de violão disponível',
    time: '2 min atrás'
  },
  {
    id: 2,
    message: 'Seu artigo foi aprovado',
    time: '1 hora atrás'
  },
  {
    id: 3,
    message: 'Lembrete: aula de piano às 15h',
    time: '3 horas atrás'
  }
])

// Computed
const isTeacherOrAdmin = computed(() => {
  return user.value.role === 'teacher' || user.value.role === 'admin'
})

// Methods
const isActiveRoute = (path) => {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
  if (showMobileMenu.value) {
    showUserMenu.value = false
    showNotifications.value = false
    showSearch.value = false
  }
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
  if (showUserMenu.value) {
    showMobileMenu.value = false
    showNotifications.value = false
    showSearch.value = false
  }
}

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
  if (showNotifications.value) {
    showUserMenu.value = false
    showMobileMenu.value = false
    showSearch.value = false
  }
}

const toggleSearch = async () => {
  showSearch.value = !showSearch.value
  if (showSearch.value) {
    showUserMenu.value = false
    showMobileMenu.value = false
    showNotifications.value = false
    await nextTick()
    searchInput.value?.focus()
  }
}

const closeSearch = () => {
  showSearch.value = false
  searchQuery.value = ''
}



const logout = () => {
  isLoggedIn.value = false
  user.value = {}
  showUserMenu.value = false
  router.push('/auth')
}

const closeMenus = (event) => {
  const clickedElement = event.target
  const isInsideDropdown = clickedElement.closest('.relative')
  
  if (!isInsideDropdown) {
    showUserMenu.value = false
    showNotifications.value = false
  }
}

// Event listeners
onMounted(() => {
  document.addEventListener('click', closeMenus)
  
  // Close search on escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      showSearch.value = false
      showMobileMenu.value = false
      showUserMenu.value = false
      showNotifications.value = false
    }
  })
})

onUnmounted(() => {
  document.removeEventListener('click', closeMenus)
})

// Close menus when route changes
watch(() => route.path, () => {
  showUserMenu.value = false
  showMobileMenu.value = false
  showNotifications.value = false
  showSearch.value = false
})

// Search functionality
watch(searchQuery, (newQuery) => {
  if (newQuery.length > 2) {
    // Implement search logic here
    console.log('Searching for:', newQuery)
  }
})
</script>

<style scoped>
/* Custom scrollbar for notifications */
.max-h-64::-webkit-scrollbar {
  width: 4px;
}

.max-h-64::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.max-h-64::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.max-h-64::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Backdrop blur fallback */
@supports not (backdrop-filter: blur(12px)) {
  nav {
    background-color: rgba(255, 255, 255, 0.95);
  }
}
</style>
