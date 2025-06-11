<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold text-gray-900 mb-2">Meu Perfil</h1>
            <p class="text-gray-600">Gerencie suas informações pessoais e acompanhe seu progresso</p>
          </div>
          
          <button 
            @click="toggleEditMode" 
            :disabled="isSaving"
            :class="[
              'px-6 py-2 rounded-lg transition-colors flex items-center gap-2',
              isSaving ? 'bg-gray-400 cursor-not-allowed' : 
              (isEditing ? 'bg-green-600 text-white hover:bg-green-700' : 'bg-blue-600 text-white hover:bg-blue-700')
            ]"
          >
            <component :is="isEditing ? Save : Edit" class="h-5 w-5" />
            {{ isSaving ? 'Salvando...' : (isEditing ? 'Salvar Alterações' : 'Editar Perfil') }}
          </button>
        </div>
      </div>

      <div class="grid lg:grid-cols-3 gap-6">
        <!-- Left Column - Profile Info -->
        <div class="lg:col-span-1 space-y-6">
          <!-- Profile Picture & Basic Info -->
          <div class="bg-white rounded-lg shadow-sm p-6">
            <div class="text-center">
              <!-- Profile Picture -->
              <div class="relative inline-block mb-4">
                <div class="w-32 h-32 rounded-full overflow-hidden bg-gray-200 mx-auto relative">
                  <img 
                    v-if="userProfile.avatar" 
                    :src="userProfile.avatar" 
                    :alt="userProfile.name"
                    class="w-full h-full object-cover"
                  >
                  <div v-else class="w-full h-full flex items-center justify-center">
                    <User class="h-16 w-16 text-gray-400" />
                  </div>
                  
                  <!-- Edit Photo Button -->
                  <button 
                    v-if="isEditing"
                    @click="$refs.avatarInput.click()"
                    class="absolute bottom-0 left-1/2 -translate-x-1/2 p-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-colors shadow-lg"
                  >
                    <Camera class="h-4 w-4" />
                  </button>
                </div>
                
                <input 
                  ref="avatarInput"
                  type="file" 
                  accept="image/*"
                  @change="handleAvatarUpload"
                  class="hidden"
                >
              </div>

              <!-- Name -->
              <div v-if="!isEditing">
                <h2 class="text-2xl font-bold text-gray-900">{{ userProfile.first_name }} {{ userProfile.last_name }}</h2>
                <p class="text-gray-600 mt-1">{{ userProfile.email }}</p>
                <div class="flex items-center justify-center gap-2 mt-2">
                  <span class="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                    {{ userProfile.skill_level }}
                  </span>
                  <span class="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">
                    {{ userProfile.gender === 'M' ? 'Masculino' : userProfile.gender === 'F' ? 'Feminino' : 'Outro' }}
                  </span>
                </div>
              </div>

              <!-- Edit Form -->
              <div v-else class="space-y-4">
                <div class="grid grid-cols-2 gap-3">
                  <input 
                    v-model="editForm.first_name" 
                    type="text" 
                    placeholder="Nome"
                    class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  >
                  <input 
                    v-model="editForm.last_name" 
                    type="text" 
                    placeholder="Sobrenome"
                    class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                  >
                </div>
                
                <select 
                  v-model="editForm.gender" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                >
                  <option value="">Selecione o sexo</option>
                  <option value="M">Masculino</option>
                  <option value="F">Feminino</option>
                  <option value="O">Outro</option>
                  <option value="N">Prefiro não informar</option>
                </select>

                <input 
                  v-model="editForm.email" 
                  type="email" 
                  placeholder="Email"
                  class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
                >
              </div>
            </div>

            <!-- Stats -->
            <div class="grid grid-cols-3 gap-4 mt-6 pt-6 border-t border-gray-200">
              <div class="text-center">
                <div class="text-2xl font-bold text-blue-600">{{ userProfile.lessons_counter }}</div>
                <div class="text-sm text-gray-600">Cursos</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-green-600">{{ userProfile.completed_tasks_counter }}</div>
                <div class="text-sm text-gray-600">Tarefas concluídas</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold text-purple-600">{{ userProfile.instruments_counter }}</div>
                <div class="text-sm text-gray-600">Instrumentos</div>
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="bg-white rounded-lg shadow-sm p-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Ações Rápidas</h3>
            <div class="space-y-3">
              <router-link 
                to="/manage-instruments" 
                class="flex items-center gap-3 p-3 bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100 transition-colors"
              >
                <Music class="h-5 w-5" />
                <span>Gerenciar Instrumentos</span>
                <ChevronRight class="h-4 w-4 ml-auto" />
              </router-link>
              
              <router-link 
                to="/courses" 
                class="flex items-center gap-3 p-3 bg-green-50 text-green-700 rounded-lg hover:bg-green-100 transition-colors"
              >
                <BookOpen class="h-5 w-5" />
                <span>Ver Todos os Cursos</span>
                <ChevronRight class="h-4 w-4 ml-auto" />
              </router-link>
              
              <router-link 
                to="/articles/create" 
                class="flex items-center gap-3 p-3 bg-purple-50 text-purple-700 rounded-lg hover:bg-purple-100 transition-colors"
              >
                <PenTool class="h-5 w-5" />
                <span>Criar Artigo</span>
                <ChevronRight class="h-4 w-4 ml-auto" />
              </router-link>
            </div>
          </div>
        </div>

        <!-- Right Column - Dashboard -->
        <div class="lg:col-span-2 space-y-6">
          <div class="bg-white rounded-lg shadow-sm p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-xl font-semibold text-gray-900">Cursos em Andamento</h3>
              <router-link to="/courses" class="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center gap-1">
                Ver todos
                <ChevronRight class="h-4 w-4" />
              </router-link>
            </div>

            <div v-if="areCoursesLoading" class="text-center py-8 text-gray-600">
              Carregando seus cursos...
            </div>

            <div v-else-if="coursesError" class="text-center py-8 text-red-600">
              {{ coursesError }}
            </div>

            <div v-else-if="inProgressCourses.length > 0" class="grid md:grid-cols-2 gap-4">
              <div v-for="course in inProgressCourses" :key="course.id" class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                <div class="flex items-start gap-4">
                  <img :src="course.cover" :alt="course.title" class="w-16 h-16 rounded-lg object-cover">
                  <div class="flex-1 min-w-0">
                    <h4 class="font-semibold text-gray-900 truncate">{{ course.title }}</h4>
                    <p class="text-sm text-gray-600 mb-2">{{ course.instructor_name }}</p>
                    
                    <div class="space-y-1">
                      <div class="flex justify-between text-sm">
                        <span class="text-gray-600">Progresso</span>
                        <span class="font-medium">{{ course.progress }}%</span>
                      </div>
                      <div class="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          class="bg-blue-600 h-2 rounded-full transition-all duration-300" 
                          :style="{ width: course.progress + '%' }"
                        ></div>
                      </div>
                    </div>
                    
                    <div class="flex items-center justify-end mt-3">
                      <button 
                        @click="continueCourse(course)"
                        class="px-3 py-1 bg-blue-600 text-white text-xs rounded-lg hover:bg-blue-700 transition-colors"
                      >
                        Continuar
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-else class="text-center py-8">
              <BookOpen class="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h4 class="text-lg font-medium text-gray-900 mb-2">Nenhum curso em andamento</h4>
              <p class="text-gray-600 mb-4">Comece sua jornada musical hoje mesmo!</p>
              <router-link to="/courses" class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                Explorar Cursos
              </router-link>
            </div>
          </div>

          <!-- My Instruments -->
          <div class="bg-white rounded-lg shadow-sm p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-xl font-semibold text-gray-900">Meus Instrumentos</h3>
              <router-link to="/manage-instruments" class="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center gap-1">
                Gerenciar
                <ChevronRight class="h-4 w-4" />
              </router-link>
            </div>

            <div v-if="areInstrumentsLoading" class="text-center py-8 text-gray-600">
              Carregando seus instrumentos...
            </div>

            <div v-else-if="instrumentsError" class="text-center py-8 text-red-600">
              {{ instrumentsError }}
            </div>

            <div v-else-if="myInstruments.length > 0" class="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div v-for="instrument in myInstruments" :key="instrument.id" class="border border-gray-200 rounded-lg p-4 text-center hover:shadow-md transition-shadow relative">
                <div 
                  v-if="instrument.color"
                  class="absolute top-2 left-2 w-4 h-4 rounded-full border border-gray-200"
                  :style="{ backgroundColor: instrument.color }"
                  :title="instrument.color"
                ></div>
                <img :src="instrument.main_image" :alt="instrument.name" class="w-20 h-20 rounded-lg object-cover mx-auto mb-3">
                <h4 class="font-semibold text-gray-900 mb-1">{{ instrument.name }}</h4>
                <p class="text-sm text-gray-600">{{ instrument.brand_name }} | {{ instrument.type_name }}</p>
              </div>
            </div>

            <div v-else class="text-center py-8">
              <Music class="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h4 class="text-lg font-medium text-gray-900 mb-2">Nenhum instrumento cadastrado</h4>
              <p class="text-gray-600 mb-4">Adicione seus instrumentos para melhor organização</p>
              <router-link to="/manage-instruments" class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                Adicionar Instrumento
              </router-link>
            </div>
          </div>

          <!-- Recent Activity -->
          <div class="bg-white rounded-lg shadow-sm p-6">
            <h3 class="text-xl font-semibold text-gray-900 mb-6">Atividade Recente</h3>
            
            <div v-if="isActivityLoading" class="text-center text-gray-500">Carregando...</div>

            <div v-else-if="activityError" class="text-center text-red-500">{{ activityError }}</div>

            <div v-else-if="recentActivity.length > 0" class="space-y-4">
              <div v-for="activity in recentActivity" :key="activity.id" class="flex items-start gap-4 p-3 bg-gray-50 rounded-lg">
                <div :class="[
                    'p-2 rounded-full',
                    // A lógica de cor pode ser baseada na ação
                    activity.action.includes('INSTRUMENT') ? 'bg-green-100 text-green-600' :
                    activity.action.includes('ARTICLE') ? 'bg-purple-100 text-purple-600' :
                    'bg-blue-100 text-blue-600'
                  ]">
                  <component :is="getActivityIcon(activity.action)" class="h-4 w-4" />
                </div>
                
                <div class="flex-1">
                  <p class="text-sm text-gray-900">{{ activity.description }}</p>
                  <p class="text-xs text-gray-500 mt-1">{{ formatRelativeTime(new Date(activity.created_at)) }}</p>
                </div>
              </div>
            </div>

            <div v-else class="text-center text-gray-500 py-4">Nenhuma atividade recente.</div>
          </div>

          <!-- Learning Goals -->
          <div class="bg-white rounded-lg shadow-sm p-6">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-xl font-semibold text-gray-900">Metas de Aprendizado</h3>
              <button @click="showGoalsModal = true" class="text-blue-600 hover:text-blue-700 text-sm font-medium flex items-center gap-1">
                <Plus class="h-4 w-4" />
                Nova Meta
              </button>
            </div>

            <div v-if="areGoalsLoading" class="text-center text-gray-500">Carregando metas...</div>
            <div v-else-if="goalsError" class="text-center text-red-500">{{ goalsError }}</div>
            
            <div v-else-if="learningGoals.length > 0" class="space-y-4">
              <div v-for="goal in learningGoals" :key="goal.id" class="border border-gray-200 rounded-lg p-4">
                <div class="flex items-start justify-between mb-3">
                  <div>
                    <h4 class="font-semibold text-gray-900">{{ goal.title }}</h4>
                    <p class="text-sm text-gray-600">{{ goal.description }}</p>
                  </div>
                  <button 
                    @click="confirmDeleteGoal(goal)"
                    class="p-2 text-gray-400 hover:text-red-600 transition-colors border border-gray-200 rounded-lg hover:bg-red-50 hover:border-red-200"
                    title="Excluir meta"
                  >
                    <X class="h-5 w-5" />
                  </button>
                </div>
                
                <div class="space-y-1">
                  <div class="flex justify-between text-sm">
                    <span class="text-gray-600">Progresso (por tempo)</span>
                    <span class="font-medium">{{ goal.progress }}%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-600 h-2 rounded-full" :style="{ width: goal.progress + '%' }"></div>
                  </div>
                </div>
                
                <div class="flex items-center justify-between mt-3 text-xs text-gray-500">
                  <span>Prazo: {{ formatDate(goal.to_do_date) }}</span>
                  <span>{{ goal.daysLeft }} dias restantes</span>
                </div>
              </div>
            </div>
            
            <div v-else class="text-center text-gray-500 py-4">Nenhuma meta definida. Crie uma para começar!</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Goals Modal -->
    <div v-if="showGoalsModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white rounded-lg w-full max-w-md mx-4 shadow-xl">
        <div class="p-6 border-b border-gray-200 flex justify-between items-center">
          <h3 class="text-lg font-semibold">Nova Meta de Aprendizado</h3>
          <button @click="showGoalsModal = false" class="text-gray-400 hover:text-gray-600">&times;</button>
        </div>
        
        <div class="p-6">
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Título da Meta</label>
              <input 
                v-model="newGoal.title"
                type="text" 
                placeholder="Ex: Aprender 5 acordes básicos"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Descrição</label>
              <textarea 
                v-model="newGoal.description"
                rows="3"
                placeholder="Descreva sua meta em detalhes..."
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              ></textarea>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Prazo</label>
              <input 
                v-model="newGoal.deadline"
                type="date" 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
            </div>
          </div>
          
          <div class="flex gap-3 mt-6">
            <button 
              @click="showGoalsModal = false"
              class="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Cancelar
            </button>
            <button 
              @click="addGoal"
              :disabled="isCreatingGoal"
              class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:bg-blue-400 disabled:cursor-not-allowed"
            >
              {{ isCreatingGoal ? 'Criando...' : 'Criar Meta' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Goal Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
      <div class="bg-white rounded-lg w-full max-w-sm mx-4 shadow-xl">
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Confirmar Exclusão</h3>
          <p class="text-gray-600 mb-6">Tem certeza que deseja excluir a meta "{{ goalToDelete?.title }}"? Esta ação não pode ser desfeita.</p>
          
          <div class="flex gap-3">
            <button 
              @click="showDeleteModal = false"
              class="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Cancelar
            </button>
            <button 
              @click="deleteGoal"
              :disabled="isDeletingGoal"
              class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:bg-red-400 disabled:cursor-not-allowed"
            >
              {{ isDeletingGoal ? 'Excluindo...' : 'Excluir Meta' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getProfile, updateProfile, getInProgressCourses, getMyInstruments, getRecentActivity, getGoals, createGoal, deleteGoal as deleteGoalApi } from '@/services/profileService';
import { 
  User, 
  Edit, 
  Save, 
  Camera, 
  Music, 
  BookOpen, 
  PenTool, 
  ChevronRight, 
  Plus,
  X,
  Target,
  Clock,
  Award
} from 'lucide-vue-next';
import { useAuthStore } from '@/stores/auth.store';

const router = useRouter()
const isEditing = ref(false)
const showGoalsModal = ref(false)
const avatarInput = ref(null)
const userProfile = ref({});
const editForm = ref({});
const newAvatarFile = ref(null);

const isProfileLoading = ref(true);
const areCoursesLoading = ref(true);
const isSaving = ref(false);

// --- NOVO: Estados para os instrumentos ---
const myInstruments = ref([]);
const areInstrumentsLoading = ref(true);
const instrumentsError = ref(null);

// --- NOVO: Estados para a atividade recente ---
const recentActivity = ref([]);
const isActivityLoading = ref(true);
const activityError = ref(null);

// --- NOVO: Estados para as metas ---
const learningGoals = ref([]);
const areGoalsLoading = ref(true);
const goalsError = ref(null);

const newGoal = ref({ title: '', description: '', deadline: '' });
const isCreatingGoal = ref(false); // para o estado de loading do botão de criar

const authStore = useAuthStore();

const inProgressCourses = ref([]);
const coursesError = ref(null); // Estado para erros ao buscar cursos

// Estados para o modal de exclusão
const showDeleteModal = ref(false);
const goalToDelete = ref(null);
const isDeletingGoal = ref(false);

const fetchProfile = async () => {
  try {
    // Não precisa setar isLoading aqui, já começa como true
    const response = await getProfile();
    const profileData = response.data;
    
    // Constrói a URL completa da imagem de perfil
    if (profileData.profile_picture) {
      // Assumindo que a API está em http://127.0.0.1:8000
      profileData.avatar = `http://127.0.0.1:8000${profileData.profile_picture}`;
    } else {
      profileData.avatar = null;
    }

    userProfile.value = profileData;
    editForm.value = { ...profileData };
    
  } catch (error) {
    console.error('Erro ao buscar perfil:', error);
    // TODO: Mostrar uma mensagem de erro para o usuário
  } finally {
    isProfileLoading.value = false;
  }
};

const fetchCourses = async () => {
  areCoursesLoading.value = true;
  coursesError.value = null;
  try {
    const response = await getInProgressCourses();
    inProgressCourses.value = response.data;

  } catch (error) {
    console.error('Erro ao buscar cursos em andamento:', error);
    coursesError.value = 'Não foi possível carregar os cursos.';
  } finally {
    areCoursesLoading.value = false;
  }
};

const fetchMyInstruments = async () => {
  areInstrumentsLoading.value = true;
  instrumentsError.value = null;
  try {
    const response = await getMyInstruments();
    myInstruments.value = response.data;
  } catch (error) {
    console.error('Erro ao buscar instrumentos:', error);
    instrumentsError.value = 'Não foi possível carregar seus instrumentos.';
  } finally {
    areInstrumentsLoading.value = false;
  }
};

const fetchRecentActivity = async () => {
  isActivityLoading.value = true;
  activityError.value = null;
  try {
    const response = await getRecentActivity();
    recentActivity.value = response.data;
  } catch (error) {
    console.error('Erro ao buscar atividades recentes:', error);
    activityError.value = 'Não foi possível carregar as atividades.';
  } finally {
    isActivityLoading.value = false;
  }
};

const fetchGoals = async () => {
  areGoalsLoading.value = true;
  goalsError.value = null;
  try {
    const response = await getGoals();
    learningGoals.value = response.data;
  } catch (error) {
    console.error('Erro ao buscar metas:', error);
    goalsError.value = 'Não foi possível carregar as metas.';
  } finally {
    areGoalsLoading.value = false;
  }
};

// --- CHAMA A FUNÇÃO AO MONTAR O COMPONENTE ---
onMounted(() => {
  fetchProfile();
  fetchCourses();
  fetchMyInstruments();
  fetchRecentActivity();
  fetchGoals();
});


// --- LÓGICA DE EDIÇÃO E SALVAMENTO (sem alterações, já estava correta) ---
const toggleEditMode = async () => {
  if (isEditing.value) {
    isSaving.value = true;
    const formData = new FormData();
    
    formData.append('first_name', editForm.value.first_name || '');
    formData.append('last_name', editForm.value.last_name || '');
    formData.append('gender', editForm.value.gender || '');
    
    if (editForm.value.bio) formData.append('bio', editForm.value.bio);
    if (editForm.value.birthday) formData.append('birthday', editForm.value.birthday);
    if (editForm.value.skill_level) formData.append('skill_level', editForm.value.skill_level);
    if (newAvatarFile.value) formData.append('profile_picture', newAvatarFile.value);

    try {
      const response = await updateProfile(formData);

      const updatedProfileData = response.data;
      if (updatedProfileData.profile_picture) {
        updatedProfileData.avatar = `http://127.0.0.1:8000${updatedProfileData.profile_picture}`;
      } else {
        updatedProfileData.avatar = null;
      }

      authStore.updateUser(updatedProfileData);
      userProfile.value = updatedProfileData;
      isEditing.value = false;
      newAvatarFile.value = null;
    } catch (error) {
      console.error('Erro ao atualizar o perfil:', error.response?.data || error);
      alert('Não foi possível salvar as alterações. Verifique os dados e tente novamente.');
    } finally {
      isSaving.value = false;
    }
  } else {
    editForm.value = { ...userProfile.value };
    isEditing.value = true;
  }
};

// --- UPLOAD DO AVATAR (sem alterações, já estava correta) ---
const handleAvatarUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  if (!file.type.startsWith('image/')) {
    alert('Por favor, selecione apenas arquivos de imagem.');
    return;
  }
  if (file.size > 5 * 1024 * 1024) {
    alert('O arquivo deve ter no máximo 5MB.');
    return;
  }

  newAvatarFile.value = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    editForm.value.avatar = e.target.result;
  };
  reader.readAsDataURL(file);
};


const continueCourse = (course) => {
  // Redireciona para a página principal da lição (curso)
  // A página de destino pode então decidir qual tarefa mostrar.
  router.push(`/lessons/${course.id}`);
}


const getActivityIcon = (action) => {
  const actionType = action.split('_')[0].toLowerCase(); // ex: 'ADD_INSTRUMENT' -> 'add'
  
  // Mapeia o tipo de ação para o tipo de ícone
  if (action.includes('INSTRUMENT')) return Music;
  if (action.includes('LESSON') || action.includes('TASK')) return BookOpen;
  if (action.includes('ARTICLE')) return PenTool;

  return BookOpen; // Ícone padrão
};

const getGoalStatusLabel = (status) => {
  const labels = {
    completed: 'Concluída',
    in_progress: 'Em Andamento',
    pending: 'Pendente'
  }
  return labels[status] || status
}

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('pt-BR', { 
    day: 'numeric', 
    month: 'short',
    year: 'numeric',
    timeZone: 'UTC' // Importante para evitar problemas de fuso horário
  }).format(date);
};

// --- MUDANÇA: Lógica do modal para criar a meta via API ---
const addGoal = async () => {
  if (!newGoal.value.title || !newGoal.value.deadline) {
    alert('Por favor, preencha pelo menos o título e o prazo.');
    return;
  }
  isCreatingGoal.value = true;
  try {
    // Chama a função do service para criar a meta no backend
    await createGoal(newGoal.value);
    
    // Sucesso! Fecha o modal, reseta o formulário e busca a lista atualizada
    showGoalsModal.value = false;
    newGoal.value = { title: '', description: '', deadline: '' };
    await fetchGoals(); // Re-busca a lista para incluir a nova meta
    
  } catch (error) {
    console.error('Erro ao criar meta:', error.response?.data || error);
    alert('Ocorreu um erro ao criar a meta. Tente novamente.');
  } finally {
    isCreatingGoal.value = false;
  }
};

const formatRelativeTime = (date) => {
  const now = new Date()
  const diffInHours = Math.floor((now - date) / (1000 * 60 * 60))
  
  if (diffInHours < 1) return 'Agora mesmo'
  if (diffInHours < 24) return `${diffInHours}h atrás`
  
  const diffInDays = Math.floor(diffInHours / 24)
  if (diffInDays < 7) return `${diffInDays}d atrás`
  
  return formatDate(date)
}

const confirmDeleteGoal = (goal) => {
  goalToDelete.value = goal;
  showDeleteModal.value = true;
};

const deleteGoal = async () => {
  if (!goalToDelete.value) return;
  
  isDeletingGoal.value = true;
  try {
    await deleteGoalApi(goalToDelete.value.id);
    await fetchGoals(); // Recarrega a lista de metas
    showDeleteModal.value = false;
    goalToDelete.value = null;
  } catch (error) {
    console.error('Erro ao excluir meta:', error);
    alert('Não foi possível excluir a meta. Tente novamente.');
  } finally {
    isDeletingGoal.value = false;
  }
};

</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>