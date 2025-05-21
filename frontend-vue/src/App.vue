<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <header class="bg-emerald-700 text-white shadow-md">
      <div class="container mx-auto px-4 py-3">
        <div class="flex flex-col md:flex-row md:justify-between md:items-center">
          <div class="flex items-center justify-between">
            <router-link to="/" class="flex items-center">
              <MusicIcon class="h-8 w-8 mr-2" />
              <span class="text-xl font-bold">MusicaMaster</span>
            </router-link>
            <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden">
              <MenuIcon v-if="!mobileMenuOpen" class="h-6 w-6" />
              <XIcon v-else class="h-6 w-6" />
            </button>
          </div>
          
          <nav :class="{'hidden': !mobileMenuOpen, 'flex': mobileMenuOpen}" class="flex-col md:flex md:flex-row mt-4 md:mt-0">
            <router-link
              v-for="(item, index) in navItems"
              :key="index"
              :to="item.path"
              @click="mobileMenuOpen = false"
              active-class="bg-emerald-800"
              class="px-4 py-2 rounded-md hover:bg-emerald-800 transition-colors cursor-pointer mb-1 md:mb-0 md:mr-1"
            >
              {{ item.name }}
            </router-link>
            
            <div v-if="isLoggedIn" class="relative">
              <button 
                @click="userMenuOpen = !userMenuOpen" 
                class="flex items-center px-4 py-2 rounded-md hover:bg-emerald-800 transition-colors cursor-pointer mb-1 md:mb-0 md:mr-1"
              >
                <UserIcon class="h-5 w-5 mr-1" />
                <span>{{ userType === 'student' ? 'Minha Conta' : 'Área do Voluntário' }}</span>
              </button>
              
              <div v-if="userMenuOpen" class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-20">
                <router-link 
                  to="/perfil" 
                  @click="userMenuOpen = false" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                >
                  Perfil
                </router-link>
                <router-link 
                  v-if="userType === 'volunteer'" 
                  to="/gerenciar/instrumentos" 
                  @click="userMenuOpen = false" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                >
                  Gerenciar Instrumentos
                </router-link>
                <router-link 
                  v-if="userType === 'volunteer'" 
                  to="/gerenciar/agenda" 
                  @click="userMenuOpen = false" 
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                >
                  Gerenciar Agenda
                </router-link>
                <a 
                  @click="handleLogout"  
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 cursor-pointer"
                >
                  Sair
                </a>
              </div>
            </div>
            
            <a 
              v-if="!isLoggedIn"
              @click="openLoginModal" 
              class="px-4 py-2 rounded-md bg-emerald-600 hover:bg-emerald-500 transition-colors cursor-pointer mt-2 md:mt-0 md:ml-2"
            >
              Entrar
            </a>
          </nav>
        </div>
      </div>
    </header>

    <div v-if="showLoginModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold">Entrar</h2>
          <button @click="showLoginModal = false" class="text-gray-500 hover:text-gray-700">
            <XIcon class="h-5 w-5" />
          </button>
        </div>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input type="email" v-model="loginEmail" class="w-full px-3 py-2 border border-gray-300 rounded-md" placeholder="seu@email.com" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Senha</label>
            <input type="password" v-model="loginPassword" class="w-full px-3 py-2 border border-gray-300 rounded-md" placeholder="********" />
          </div>
          <div class="flex items-center">
            <input type="checkbox" id="user-type-login" v-model="isVolunteerLogin" class="h-4 w-4 text-emerald-600 border-gray-300 rounded" />
            <label for="user-type-login" class="ml-2 block text-sm text-gray-700">Entrar como ONG/Professor Voluntário</label>
          </div>
          <div class="flex justify-between">
            <button @click="handleLogin" class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">Entrar</button>
            <button class="text-emerald-600 hover:text-emerald-500">Esqueci minha senha</button>
          </div>
        </div>
      </div>
    </div>

    <main class="flex-grow container mx-auto px-4 py-8">
      <router-view v-slot="{ Component, route }">
        <transition name="fade" mode="out-in">
          <component 
            :is="Component" 
            :key="route.path" 
            :isLoggedIn="isLoggedIn" 
            :userType="userType"
            @openLoginModal="openLoginModal"
            @openAddInstrumentModal="openAddInstrumentModal"
          />
        </transition>
      </router-view>
    </main>

    <div v-if="showAddInstrumentModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
       <div class="bg-white rounded-lg p-6 w-full max-w-md">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold">Adicionar Instrumento</h2>
            <button @click="showAddInstrumentModal = false" class="text-gray-500 hover:text-gray-700">
              <XIcon class="h-5 w-5" />
            </button>
          </div>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Nome do Instrumento</label>
              <input type="text" v-model="newInstrument.name" class="w-full px-3 py-2 border border-gray-300 rounded-md" placeholder="Ex: Violão Clássico" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
              <textarea v-model="newInstrument.description" class="w-full px-3 py-2 border border-gray-300 rounded-md" placeholder="Descreva o instrumento, condições, etc." rows="3"></textarea>
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Instrumento</label>
              <select v-model="newInstrument.type" class="w-full px-3 py-2 border border-gray-300 rounded-md">
                <option>Cordas</option> <option>Percussão</option> <option>Sopro</option> <option>Teclas</option> <option>Outro</option>
              </select>
            </div>
            <div class="flex items-center">
              <input type="checkbox" id="instrument-available" v-model="newInstrument.available" class="h-4 w-4 text-emerald-600 border-gray-300 rounded" />
              <label for="instrument-available" class="ml-2 block text-sm text-gray-700">Disponível para uso</label>
            </div>
            <div class="flex justify-end">
              <button @click="showAddInstrumentModal = false" class="px-4 py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors mr-2">Cancelar</button>
              <button @click="addInstrument" class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">Adicionar</button>
            </div>
          </div>
        </div>
    </div>

    <footer class="bg-gray-800 text-white py-8">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 class="text-lg font-semibold mb-4">MusicaMaster</h3>
            <p class="text-gray-400">Sua jornada musical começa aqui. Aprenda, pratique e evolua com nossos recursos exclusivos.</p>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-4">Links Rápidos</h3>
            <ul class="space-y-2">
              <li v-for="(item, index) in navItems" :key="index">
                <router-link :to="item.path" class="text-gray-400 hover:text-white cursor-pointer">{{ item.name }}</router-link>
              </li>
            </ul>
          </div>
          <div>
            <h3 class="text-lg font-semibold mb-4">Contato</h3>
            <p class="text-gray-400 mb-2">contato@musicamaster.com</p>
            <p class="text-gray-400">+55 (XX) XXXXX-XXXX</p>
            <div class="flex space-x-4 mt-4">
              <a href="#" class="text-gray-400 hover:text-white"><FacebookIcon class="h-5 w-5" /></a>
              <a href="#" class="text-gray-400 hover:text-white"><InstagramIcon class="h-5 w-5" /></a>
              <a href="#" class="text-gray-400 hover:text-white"><YoutubeIcon class="h-5 w-5" /></a>
            </div>
          </div>
        </div>
        <div class="border-t border-gray-700 mt-8 pt-6 text-center text-gray-400">
          <p>&copy; {{ new Date().getFullYear() }} MusicaMaster. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { 
  Music as MusicIcon, 
  Menu as MenuIcon, 
  X as XIcon, 
  User as UserIcon,
  Facebook as FacebookIcon,
  Instagram as InstagramIcon,
  Youtube as YoutubeIcon
} from 'lucide-vue-next';

const router = useRouter();

const mobileMenuOpen = ref(false);
const userMenuOpen = ref(false);
const showLoginModal = ref(false);
const showAddInstrumentModal = ref(false);

const isLoggedIn = ref(false);
const userType = ref('student'); // 'student' or 'volunteer'

const loginEmail = ref('');
const loginPassword = ref('');
const isVolunteerLogin = ref(false);

const newInstrument = ref({
  name: '',
  description: '',
  type: 'Cordas',
  available: true,
});

const navItems = [
  { name: 'Início', path: '/' },
  { name: 'Artigos', path: '/artigos' },
  { name: 'Instrumentos', path: '/instrumentos' },
  { name: 'Cursos', path: '/cursos' }
];

const openLoginModal = () => {
  showLoginModal.value = true;
};

const openAddInstrumentModal = () => {
  // Idealmente, esta função seria chamada por um evento emitido pela ManageInstrumentsPage
  // se o botão "Adicionar Instrumento" estiver naquela página.
  // Se o botão estiver no App.vue (improvável para este caso), então é direto.
  showAddInstrumentModal.value = true;
};

const handleLogin = () => {
  // Lógica de autenticação simulada. Substitua pela sua real.
  console.log('Tentando login com:', loginEmail.value, 'Voluntário:', isVolunteerLogin.value);
  isLoggedIn.value = true;
  userType.value = isVolunteerLogin.value ? 'volunteer' : 'student';
  
  localStorage.setItem('isLoggedIn', 'true');
  localStorage.setItem('userType', userType.value);

  showLoginModal.value = false;
  loginEmail.value = '';
  loginPassword.value = '';
  
  if (userType.value === 'volunteer') {
    router.push({ name: 'ManageInstruments' });
  } else {
    // Poderia redirecionar para o perfil ou dashboard do aluno
    router.push({ name: 'Profile' });
  }
};

const handleLogout = () => {
  isLoggedIn.value = false;
  userType.value = 'student';
  localStorage.removeItem('isLoggedIn');
  localStorage.removeItem('userType');
  userMenuOpen.value = false;
  router.push({ name: 'Home' });
};

const addInstrument = () => {
  // Lógica para adicionar o instrumento.
  // Em um app real, você enviaria para o backend e atualizaria uma lista (Pinia).
  console.log('Adicionando instrumento:', newInstrument.value);
  // Limpar o formulário e fechar o modal
  newInstrument.value = { name: '', description: '', type: 'Cordas', available: true };
  showAddInstrumentModal.value = false;
  // Você pode precisar emitir um evento para a ManageInstrumentsPage atualizar sua lista,
  // ou se usar Pinia, a atualização do store seria reativa.
};

// Carregar estado de login inicial do localStorage
onMounted(() => {
  isLoggedIn.value = JSON.parse(localStorage.getItem('isLoggedIn') || 'false');
  userType.value = localStorage.getItem('userType') || 'student';
});

// Observar o estado de login para fechar o menu de usuário se o usuário deslogar
watch(isLoggedIn, (newValue) => {
  if (!newValue) {
    userMenuOpen.value = false;
  }
});
</script>

<style>
/* Estilos globais e de transição */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease-out;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>