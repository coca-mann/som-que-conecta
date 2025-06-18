<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <button
              class="p-2 text-gray-600 hover:text-red-600 transition-colors"
              @click="goBack"
            >
              <ArrowLeft class="h-5 w-5" />
            </button>
            <div>
              <h1 class="text-2xl font-bold text-gray-900">
                {{ isEditing ? 'Editar Artigo' : 'Criar Novo Artigo' }}
              </h1>
              <p class="text-gray-600">
                Compartilhe seu conhecimento musical com a comunidade
              </p>
            </div>
          </div>
        </div>
      </div>

      <form
        class="space-y-6"
        @submit.prevent="handleSubmit"
      >
        <div class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">
            Informações Básicas
          </h2>
          
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">Título do Artigo *</label>
            <input 
              v-model="form.title" 
              type="text" 
              required 
              placeholder="Digite um título atrativo para seu artigo"
              class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            >
            <p class="text-xs text-gray-500 mt-1">
              {{ form.title?.length || 0 }}/100 caracteres
            </p>
          </div>

          <div class="grid md:grid-cols-3 gap-4 mb-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Categoria *</label>
              <select 
                v-model="form.category" 
                required 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              >
                <option :value="null">
                  Selecione uma categoria
                </option>
                <option
                  v-for="category in categories"
                  :key="category.id"
                  :value="category.name"
                >
                  {{ category.name }}
                </option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tempo de Leitura</label>
              <input 
                v-model.number="form.reading_time" 
                type="number" 
                min="1" 
                max="60"
                placeholder="5"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              >
              <p class="text-xs text-gray-500 mt-1">
                Em minutos
              </p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Dificuldade</label>
              <select 
                v-model="form.difficulty" 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
              >
                <option :value="null">
                  Selecione o nível de dificuldade
                </option>
                <option value="BEGINNER">
                  Iniciante
                </option>
                <option value="INTERMEDIATE">
                  Intermediário
                </option>
                <option value="ADVANCED">
                  Avançado
                </option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Resumo *</label>
            <textarea 
              v-model="form.excerpt" 
              rows="3" 
              required
              placeholder="Escreva um breve resumo que desperte o interesse do leitor..."
              maxlength="300"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent resize-none"
            />
            <p class="text-xs text-gray-500 mt-1">
              {{ form.excerpt?.length || 0 }}/300 caracteres
            </p>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">
            Imagem de Capa
          </h2>
          
          <div class="mb-4">
            <div class="flex gap-4">
              <label class="flex items-center">
                <input 
                  v-model="imageUploadMethod" 
                  type="radio" 
                  value="upload" 
                  class="mr-2 text-red-600 focus:ring-red-500"
                >
                <span class="text-sm font-medium text-gray-700">Enviar do computador</span>
              </label>
              <label class="flex items-center">
                <input 
                  v-model="imageUploadMethod" 
                  type="radio" 
                  value="url" 
                  class="mr-2 text-red-600 focus:ring-red-500"
                >
                <span class="text-sm font-medium text-gray-700">Link da internet</span>
              </label>
            </div>
          </div>

          <div class="space-y-4">
            <div class="flex items-start gap-6">
              <div class="w-48 h-32 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center bg-gray-50 relative overflow-hidden">
                <img
                  v-if="form.cover_image"
                  :src="form.cover_image"
                  alt="Preview"
                  class="w-full h-full object-cover rounded-lg"
                >
                <div
                  v-else
                  class="text-center"
                >
                  <ImageIcon class="h-8 w-8 text-gray-400 mx-auto mb-2" />
                  <span class="text-sm text-gray-500">Imagem de capa</span>
                </div>
                
                <button 
                  v-if="form.cover_image" 
                  type="button" 
                  class="absolute top-2 right-2 p-1 bg-red-600 text-white rounded-full hover:bg-red-700 transition-colors"
                  @click="removeImage"
                >
                  <X class="h-3 w-3" />
                </button>
              </div>
              
              <div class="flex-1">
                <div
                  v-if="imageUploadMethod === 'upload'"
                  class="space-y-3"
                >
                  <div>
                    <input 
                      ref="fileInput"
                      type="file" 
                      accept=".jpg,.jpeg,.png,.gif,image/jpeg,image/png,image/gif"
                      class="hidden"
                      @change="handleFileUpload"
                    >
                    <button 
                      type="button" 
                      class="w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-red-400 hover:bg-red-50 transition-colors flex items-center justify-center gap-2"
                      @click="$refs.fileInput.click()"
                    >
                      <Upload class="h-5 w-5 text-gray-400" />
                      <span class="text-gray-600">Clique para selecionar uma imagem</span>
                    </button>
                  </div>
                  
                  <div
                    v-if="uploadProgress > 0 && uploadProgress < 100"
                    class="space-y-2"
                  >
                    <div class="flex justify-between text-sm text-gray-600">
                      <span>Enviando...</span>
                      <span>{{ uploadProgress }}%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div
                        class="bg-red-600 h-2 rounded-full transition-all duration-300"
                        :style="{ width: uploadProgress + '%' }"
                      />
                    </div>
                  </div>
                  
                  <p class="text-sm text-gray-600">
                    Formatos aceitos: JPG, PNG, GIF (máx. 5MB)
                  </p>
                </div>

                <div
                  v-else
                  class="space-y-3"
                >
                  <input 
                    v-model="form.cover_link" 
                    type="url" 
                    placeholder="Cole a URL da imagem aqui"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
                    @input="handleUrlInput"
                  >
                  <p class="text-sm text-gray-600">
                    Cole o link direto de uma imagem da internet
                  </p>
                </div>
                
                <div
                  v-if="imageInfo"
                  class="mt-3 p-3 bg-gray-50 rounded-lg"
                >
                  <div class="text-sm text-gray-600 space-y-1">
                    <div v-if="imageInfo.name">
                      <strong>Nome:</strong> {{ imageInfo.name }}
                    </div>
                    <div v-if="imageInfo.size">
                      <strong>Tamanho:</strong> {{ imageInfo.size }}
                    </div>
                    <div v-if="imageInfo.dimensions">
                      <strong>Dimensões:</strong> {{ imageInfo.dimensions }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div class="bg-red-50 border border-red-200 rounded-lg p-4">
              <h4 class="text-sm font-medium text-red-900 mb-2">
                💡 Dicas para uma boa imagem de capa:
              </h4>
              <ul class="text-sm text-red-800 space-y-1">
                <li>• Use proporção 16:9 (ex: 1600x900px) para melhor visualização</li>
                <li>• Resolução mínima recomendada: 800x450px</li>
                <li>• Evite imagens com muito texto</li>
                <li>• Prefira imagens relacionadas ao conteúdo do artigo</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">
            Conteúdo do Artigo *
          </h2>
          <div class="flex justify-center">
            <div class="w-full max-w-5xl">
              <RichTextEditor v-model="form.content" />
            </div>
          </div>
          <div class="mt-2 text-sm text-gray-500">
            Palavras: {{ wordCount }} | Caracteres: {{ form.content?.length || 0 }}
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm overflow-hidden">
          <div class="px-6 py-4 bg-gray-50 border-b border-gray-200">
            <div class="flex flex-col gap-2">
              <h3 class="text-sm font-medium text-gray-700">
                Moderação
              </h3>
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2 text-sm text-gray-600">
                  <div
                    class="w-2 h-2 rounded-full"
                    :class="{
                      'bg-red-500': aiStatus === false,
                      'bg-green-500': aiStatus === true,
                      'bg-gray-500': aiStatus === null
                    }"
                  />
                  <span
                    :class="{
                      'text-red-600': aiStatus === false,
                      'text-green-600': aiStatus === true,
                      'text-gray-600': aiStatus === null
                    }"
                  >{{ aiFeedback || 'Seu artigo será revisado antes da publicação' }}</span>
                </div>
                <div class="text-xs text-gray-500">
                  Última modificação: {{ formatDate(form.modified_at) }}
                </div>
              </div>
            </div>
          </div>

          <div class="px-6 py-6">
            <div class="flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
              <div class="flex flex-wrap gap-3 order-2 sm:order-1">
                <div class="relative group">
                  <button 
                    type="button" 
                    class="inline-flex items-center gap-2 px-4 py-2.5 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-all duration-200 font-medium disabled:opacity-50 disabled:cursor-not-allowed" 
                    :disabled="!form.category"
                    @click="saveDraft"
                  >
                    <Save class="h-4 w-4" />
                    <span class="hidden sm:inline">Salvar Rascunho</span>
                    <span class="sm:hidden">Rascunho</span>
                  </button>
                  
                  <div 
                    v-if="!form.category" 
                    class="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-10"
                  >
                    Selecione uma categoria primeiro
                    <div class="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900" />
                  </div>
                </div>

                <button 
                  type="button" 
                  class="inline-flex items-center gap-2 px-4 py-2.5 bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-all duration-200 font-medium border border-red-200" 
                  @click="previewArticle"
                >
                  <Eye class="h-4 w-4" />
                  <span class="hidden sm:inline">Visualizar</span>
                  <span class="sm:hidden">Preview</span>
                </button>

                <button 
                  v-if="isEditing"
                  type="button" 
                  class="inline-flex items-center justify-center w-10 h-10 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-all duration-200 border border-red-200 group" 
                  title="Excluir artigo"
                  @click="confirmDelete"
                >
                  <Trash2 class="h-4 w-4 group-hover:scale-110 transition-transform duration-200" />
                </button>
              </div>

              <div class="flex gap-3 order-1 sm:order-2">
                <button 
                  type="button" 
                  class="px-6 py-2.5 bg-white text-gray-700 rounded-lg hover:bg-gray-50 transition-all duration-200 font-medium border border-gray-300" 
                  @click="goBack"
                >
                  Cancelar
                </button>
                <button 
                  type="submit" 
                  class="px-6 py-2.5 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-all duration-200 font-medium shadow-sm hover:shadow-md flex items-center gap-2 disabled:opacity-75 disabled:cursor-not-allowed"
                  :disabled="isLoading"
                >
                  <div
                    v-if="isLoading"
                    class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"
                  />
                  {{ isLoading ? 'Salvando...' : (isEditing ? 'Atualizar Artigo' : 'Publicar Artigo') }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </form>
    </div>

    <div
      v-if="showPreview"
      class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50"
    >
      <div class="bg-white/95 backdrop-blur-sm rounded-lg w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200 flex justify-between items-center">
          <h3 class="text-lg font-semibold">
            Visualização do Artigo
          </h3>
          <button
            class="text-gray-400 hover:text-red-600 transition-colors"
            @click="showPreview = false"
          >
            <X class="h-6 w-6" />
          </button>
        </div>
        <div class="p-6">
          <img
            v-if="form.cover_image"
            :src="form.cover_image"
            :alt="form.title"
            class="w-full h-64 object-cover rounded-lg mb-6"
          >
          <h1 class="text-3xl font-bold text-gray-900 mb-4">
            {{ form.title }}
          </h1>
          <p class="text-xl text-gray-600 mb-6">
            {{ form.excerpt }}
          </p>
          <div
            class="prose max-w-none"
            v-html="form.content"
          />
        </div>
      </div>
    </div>

    <div
      v-if="showDeleteConfirm"
      class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50"
    >
      <div class="bg-white/95 backdrop-blur-sm rounded-lg w-full max-w-md mx-4 p-6 shadow-xl">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">
          Confirmar Exclusão
        </h3>
        <p class="text-gray-600 mb-6">
          Tem certeza que deseja excluir este artigo? Esta ação não pode ser desfeita.
        </p>
        <div class="flex justify-end gap-3">
          <button 
            class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors" 
            :disabled="isDeleting"
            @click="showDeleteConfirm = false"
          >
            Cancelar
          </button>
          <button 
            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2" 
            :disabled="isDeleting"
            @click="deleteArticle"
          >
            <div
              v-if="isDeleting"
              class="animate-spin rounded-full h-4 w-4 border-b-2 border-white"
            />
            {{ isDeleting ? 'Excluindo...' : 'Excluir' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import articleService from '@/services/articleService';
import RichTextEditor from '@/components/RichTextEditor.vue';
import { 
  ArrowLeft, 
  Save, 
  Eye, 
  X, 
  Plus,
  Image as ImageIcon,
  Upload,
  Trash2
} from 'lucide-vue-next'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const editor = ref(null)
const fileInput = ref(null)
const showPreview = ref(false)
const imageUploadMethod = ref('upload')
const uploadProgress = ref(0)
const imageInfo = ref(null)
const isLoading = ref(false)
const error = ref(null)
const showDeleteConfirm = ref(false)
const isDeleting = ref(false)
const aiStatus = ref(null)
const aiFeedback = ref(null)

const isEditing = computed(() => route.params.id !== undefined);
const imageFile = ref(null);
const categories = ref([]);

const form = ref({
  title: '',
  category: null,
  excerpt: '',
  content: '',
  reading_time: 5,
  difficulty: 'BEGINNER',
  cover_image: '',
  cover_link: '',
  modified_at: null,
});

const wordCount = computed(() => {
  return form.value.content.replace(/<[^>]*>/g, '').split(/\s+/).filter(word => word.length > 0).length
})

const handleSave = async (asDraft = false) => {
  isLoading.value = true;
  error.value = null;

  const formData = new FormData();

  formData.append('title', form.value.title);
  formData.append('category_name', form.value.category);
  formData.append('short_description', form.value.excerpt);
  formData.append('content', form.value.content);
  formData.append('reading_time', form.value.reading_time);
  formData.append('difficulty', form.value.difficulty);
  formData.append('cover_link', form.value.cover_link);
  
  if (asDraft) {
    formData.append('is_draft', 'true');
    formData.append('is_published', 'false');
  } else {
    formData.append('is_draft', 'false');
    formData.append('is_published', 'true');
  }

  if (imageFile.value) {
    formData.append('cover_image', imageFile.value);
  }

  try {
    if (isEditing.value) {
      await articleService.updateArticle(route.params.id, formData);
    } else {
      await articleService.createArticle(formData);
    }
    router.push('/articles');
  } catch (err) {
    console.error("Erro ao salvar artigo:", err.response?.data || err);
    error.value = err.response?.data?.detail || "Falha ao salvar o artigo. Verifique os campos e tente novamente.";
  } finally {
    isLoading.value = false;
  }
};

const goBack = () => router.push('/articles');

const updateContent = () => {
  if (editor.value) {
    form.value.content = editor.value.innerHTML
  }
}

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;
    form.value.cover_image = URL.createObjectURL(file);
  }
};

const handleUrlInput = () => {
  if (form.value.cover_link) {
    try {
      new URL(form.value.cover_link)
      form.value.cover_image = form.value.cover_link
      
      const img = new Image()
      img.onload = () => {
        imageInfo.value = {
          dimensions: `${img.width}x${img.height}px`
        }
      }
      img.onerror = () => {
        imageInfo.value = null
      }
      img.src = form.value.cover_link
    } catch (error) {
      form.value.cover_image = ''
      imageInfo.value = null
    }
  } else {
    form.value.cover_image = ''
    imageInfo.value = null
  }
}

const removeImage = () => {
  form.value.cover_image = ''
  form.value.cover_link = ''
  imageInfo.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const saveDraft = () => {
  handleSave(true);
};

const previewArticle = () => {
  updateContent()
  showPreview.value = true
}

const handleSubmit = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    if (isEditing.value) {
      // Primeiro salva o artigo como rascunho
      const formData = new FormData();
      formData.append('title', form.value.title);
      formData.append('category_name', form.value.category);
      formData.append('short_description', form.value.excerpt);
      formData.append('content', form.value.content);
      formData.append('reading_time', form.value.reading_time);
      formData.append('difficulty', form.value.difficulty);
      formData.append('cover_link', form.value.cover_link);
      formData.append('is_draft', 'true');
      formData.append('is_published', 'false');

      if (imageFile.value) {
        formData.append('cover_image', imageFile.value);
      }

      await articleService.updateArticle(route.params.id, formData);

      // Depois submete para publicação
      const response = await articleService.submitForPublication(route.params.id);
      
      if (response.data.feedback) {
        aiStatus.value = response.data.ai_bool;
        aiFeedback.value = response.data.feedback;
        
        // Se aprovado pela IA, publica automaticamente
        if (response.data.ai_bool === true) {
          const publishData = new FormData();
          publishData.append('is_draft', 'false');
          publishData.append('is_published', 'true');
          await articleService.updateArticle(route.params.id, publishData);
          router.push('/articles');
        }
      }
    } else {
      // Primeiro cria o artigo como rascunho
      const formData = new FormData();
      formData.append('title', form.value.title);
      formData.append('category_name', form.value.category);
      formData.append('short_description', form.value.excerpt);
      formData.append('content', form.value.content);
      formData.append('reading_time', form.value.reading_time);
      formData.append('difficulty', form.value.difficulty);
      formData.append('cover_link', form.value.cover_link);
      formData.append('is_draft', 'true');
      formData.append('is_published', 'false');

      if (imageFile.value) {
        formData.append('cover_image', imageFile.value);
      }

      const createResponse = await articleService.createArticle(formData);
      
      // Verifica se temos o ID do artigo criado
      if (!createResponse.data || !createResponse.data.id) {
        throw new Error('Não foi possível obter o ID do artigo criado');
      }
      
      // Depois submete para publicação
      const response = await articleService.submitForPublication(createResponse.data.id);
      
      if (response.data.feedback) {
        aiStatus.value = response.data.ai_bool;
        aiFeedback.value = response.data.feedback;
        
        // Se aprovado pela IA, publica automaticamente
        if (response.data.ai_bool === true) {
          const publishData = new FormData();
          publishData.append('is_draft', 'false');
          publishData.append('is_published', 'true');
          await articleService.updateArticle(createResponse.data.id, publishData);
          router.push('/articles');
        }
      }
    }
  } catch (err) {
    console.error("Erro ao salvar artigo:", err.response?.data || err);
    if (err.response?.data?.feedback) {
      error.value = err.response.data.feedback;
      aiStatus.value = err.response.data.ai_bool;
      aiFeedback.value = err.response.data.feedback;
    } else {
      error.value = err.response?.data?.detail || "Falha ao salvar o artigo. Verifique os campos e tente novamente.";
    }
  } finally {
    isLoading.value = false;
  }
};

const checkPermission = () => {
  const userRole = authStore.user?.role
  const allowedRoles = ['admin', 'ong', 'teacher']
  
  if (!userRole || !allowedRoles.includes(userRole)) {
    router.push('/articles')
  }
}

const confirmDelete = () => {
  showDeleteConfirm.value = true
}

const deleteArticle = async () => {
  isDeleting.value = true
  try {
    await articleService.deleteArticle(route.params.id)
    showDeleteConfirm.value = false
    router.push('/articles')
  } catch (err) {
    console.error('Erro ao excluir artigo:', err)
    const errorMessage = err.response?.data?.detail || 'Erro ao excluir o artigo. Por favor, tente novamente.'
    alert(errorMessage)
  } finally {
    isDeleting.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return 'agora';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
}

onMounted(async () => {
  try {
    const response = await articleService.getCategories();
    categories.value = response.data;
  } catch (err) {
    console.error('Erro ao carregar categorias:', err);
  }

  if (isEditing.value) {
    try {
      const response = await articleService.getArticleDetail(route.params.id);
      const articleData = response.data;
      
      form.value.title = articleData.title;
      form.value.category = articleData.category?.name || null;
      form.value.excerpt = articleData.short_description || articleData.excerpt;
      form.value.content = articleData.content;
      form.value.reading_time = articleData.reading_time;
      form.value.difficulty = articleData.difficulty;
      form.value.modified_at = articleData.modified_at;
      aiStatus.value = articleData.ai_bool;
      aiFeedback.value = articleData.ai_feedback;
      
      if (articleData.cover_image) {
        form.value.cover_image = articleData.cover_image;
        imageUploadMethod.value = 'upload';
      } else if (articleData.cover_url) {
        form.value.cover_image = articleData.cover_url;
        form.value.cover_link = articleData.cover_url;
        imageUploadMethod.value = 'url';
      }
      
    } catch (err) {
      console.error('Erro ao carregar artigo para edição:', err);
    }
  }

  checkPermission()
});
</script>

<style scoped>
.prose h1 {
  @apply text-2xl font-bold text-gray-900 mt-6 mb-4;
}

.prose h2 {
  @apply text-xl font-bold text-gray-900 mt-6 mb-3;
}

.prose h3 {
  @apply text-lg font-semibold text-gray-900 mt-4 mb-2;
}

.prose p {
  @apply text-gray-700 leading-relaxed mb-4;
}

.prose ul, .prose ol {
  @apply list-disc list-inside space-y-1 mb-4 text-gray-700 ml-4;
}

.prose ol {
  @apply list-decimal;
}

.prose a {
  @apply text-blue-600 hover:text-blue-800 underline;
}

.prose img {
  @apply max-w-full h-auto rounded-lg my-4;
}

.prose strong {
  @apply font-semibold;
}

.prose em {
  @apply italic;
}
</style>
