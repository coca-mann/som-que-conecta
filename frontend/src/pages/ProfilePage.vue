<template>
    <div class="space-y-6">
      <h1 class="text-3xl font-bold text-emerald-800 mb-6">Seu Perfil</h1>
      
      <div v-if="!isLoggedIn" class="bg-amber-50 border border-amber-200 rounded-lg p-6 text-center">
        <LockIcon class="h-12 w-12 text-amber-500 mx-auto mb-4" />
        <h2 class="text-xl font-semibold mb-2">Acesso Restrito</h2>
        <p class="text-gray-600 mb-4">Faça login para acessar seu perfil.</p>
        <button 
          @click="emitOpenLoginModal"
          class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors"
        >
          Entrar
        </button>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="md:col-span-1">
          <div class="bg-white rounded-lg shadow-md p-6">
            <div class="flex flex-col items-center">
              <div class="w-32 h-32 bg-emerald-100 rounded-full flex items-center justify-center mb-4">
                <UserIcon class="h-16 w-16 text-emerald-600" />
              </div>
              <h2 class="text-xl font-semibold">{{ userProfile.name }}</h2>
              <p class="text-gray-500 capitalize">{{ userTypeToDisplay }}</p>
              
              <div class="w-full mt-6 space-y-2">
                <button class="w-full py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                  Editar Perfil
                </button>
                <button class="w-full py-2 border border-gray-300 rounded-md hover:bg-gray-50 transition-colors">
                  Alterar Senha
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="md:col-span-2">
          <div class="bg-white rounded-lg shadow-md p-6">
            <h3 class="text-lg font-semibold mb-4">Informações Pessoais</h3>
            <form @submit.prevent="saveProfile" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Nome Completo</label>
                <input type="text" v-model="editableProfile.name" class="w-full px-3 py-2 border border-gray-300 rounded-md" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input type="email" v-model="editableProfile.email" class="w-full px-3 py-2 border border-gray-300 rounded-md" />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">Celular</label>
                <input type="tel" v-model="editableProfile.phone" class="w-full px-3 py-2 border border-gray-300 rounded-md" />
              </div>
              
              <div v-if="userType === 'volunteer'">
                <label class="block text-sm font-medium text-gray-700 mb-1">Tipo (Voluntário)</label>
                <select v-model="editableProfile.volunteerType" class="w-full px-3 py-2 border border-gray-300 rounded-md">
                  <option value="ong">ONG</option>
                  <option value="professor">Professor Voluntário</option>
                </select>
              </div>
              
              <div v-if="userType === 'volunteer'">
                <label class="block text-sm font-medium text-gray-700 mb-1">Descrição (Voluntário)</label>
                <textarea v-model="editableProfile.description" rows="3" class="w-full px-3 py-2 border border-gray-300 rounded-md"></textarea>
              </div>
              
              <div class="pt-4">
                <button type="submit" class="px-4 py-2 bg-emerald-600 text-white rounded-md hover:bg-emerald-500 transition-colors">
                  Salvar Alterações
                </button>
              </div>
            </form>
          </div>
          
          <div v-if="userType === 'student' && enrolledCourses.length > 0" class="bg-white rounded-lg shadow-md p-6 mt-6">
            <h3 class="text-lg font-semibold mb-4">Meu Progresso nos Cursos</h3>
            <div class="space-y-4">
              <div v-for="(course, index) in enrolledCourses" :key="index" class="border-b pb-4 last:border-b-0">
                <div class="flex justify-between items-center mb-2">
                  <h4 class="font-medium">{{ course.title }}</h4>
                  <span class="text-sm text-gray-500">{{ course.progress }}% concluído</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div class="bg-emerald-600 h-2.5 rounded-full" :style="{ width: course.progress + '%' }"></div>
                </div>
                <div class="mt-2 flex justify-end">
                  <router-link 
                    :to="`/cursos/${course.id}`"
                    class="text-sm text-emerald-600 hover:text-emerald-500"
                  >
                    Continuar Curso →
                  </router-link>
                </div>
              </div>
            </div>
          </div>
           <div v-if="userType === 'student' && enrolledCourses.length === 0" class="bg-white rounded-lg shadow-md p-6 mt-6 text-center text-gray-500">
            Você ainda não está matriculado em nenhum curso.
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, defineProps, getCurrentInstance, watch } from 'vue';
  import { useRouter } from 'vue-router';
  import { Lock as LockIcon, User as UserIcon } from 'lucide-vue-next';
  
  const props = defineProps({
    isLoggedIn: Boolean,
    userType: String // 'student' or 'volunteer'
  });
  
  const instance = getCurrentInstance();
  const router = useRouter();
  
  const emitOpenLoginModal = () => {
    instance.emit('openLoginModal');
  };
  
  // Mock data - em um app real, viria do backend/store após login
  const userProfile = ref({
    name: 'Usuário Teste',
    email: 'usuario@teste.com',
    phone: '(XX) XXXXX-XXXX',
    volunteerType: 'professor', // 'ong' or 'professor'
    description: 'Amo ensinar música e ajudar a comunidade!'
  });
  
  // Para edição
  const editableProfile = ref({});
  
  // Atualiza editableProfile quando userProfile ou userType mudar
  watch([userProfile, () => props.userType], () => {
    editableProfile.value = { ...userProfile.value };
  }, { immediate: true, deep: true });
  
  
  const enrolledCoursesData = ref([ // Simulação de dados de cursos
     { id: 'violao-iniciante', title: 'Violão para Iniciantes', progress: 65 },
     { id: 'piano-fundamentos', title: 'Fundamentos do Piano', progress: 30 }
  ]);
  
  const enrolledCourses = computed(() => {
      if(props.userType === 'student') {
          // Em um app real, você filtraria os cursos do usuário
          return enrolledCoursesData.value;
      }
      return [];
  });
  
  const userTypeToDisplay = computed(() => {
      if (props.userType === 'student') return 'Estudante';
      if (props.userType === 'volunteer') return 'Voluntário';
      return 'Usuário';
  });
  
  const saveProfile = () => {
    // Lógica para salvar o perfil (ex: chamada API)
    console.log('Salvando perfil:', editableProfile.value);
    // Atualizar userProfile com editableProfile após salvar com sucesso
    userProfile.value = { ...editableProfile.value };
    alert('Perfil salvo com sucesso! (Simulação)');
  };
  
  // Se o usuário não estiver logado e tentar acessar, redirecionar ou mostrar mensagem
  onMounted(() => {
    if (!props.isLoggedIn) {
      // O guarda de rota já deve ter lidado com isso, mas como fallback:
      // emitOpenLoginModal(); // Ou redirecionar
      // router.push('/');
    } else {
       // Carregar dados do perfil real aqui se não mockado globalmente
    }
  });
  </script>