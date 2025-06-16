<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Header -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <button @click="goBack" class="p-2 text-gray-600 hover:text-blue-600 transition-colors">
              <ArrowLeft class="h-5 w-5" />
            </button>
            <div>
              <h1 class="text-2xl font-bold text-gray-900">
                {{ isEditing ? 'Editar Artigo' : 'Criar Novo Artigo' }}
              </h1>
              <p class="text-gray-600">Compartilhe seu conhecimento musical com a comunidade</p>
            </div>
          </div>
          
          <div class="flex items-center gap-3">
            <button @click="saveDraft" class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
              <Save class="h-4 w-4 inline mr-2" />
              Salvar Rascunho
            </button>
            <button @click="previewArticle" class="px-4 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors">
              <Eye class="h-4 w-4 inline mr-2" />
              Visualizar
            </button>
          </div>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <!-- Article Header -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Informações Básicas</h2>
          
          <!-- Title -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">Título do Artigo *</label>
            <input 
              v-model="form.title" 
              type="text" 
              required 
              placeholder="Digite um título atrativo para seu artigo"
              class="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
            <p class="text-xs text-gray-500 mt-1">{{ form.title.length }}/100 caracteres</p>
          </div>

          <!-- Category and Reading Time -->
          <div class="grid md:grid-cols-3 gap-4 mb-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Categoria *</label>
              <select 
                v-model="form.category" 
                required 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option :value="null">Selecione uma categoria</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
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
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
              <p class="text-xs text-gray-500 mt-1">Em minutos</p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Dificuldade</label>
              <select 
                v-model="form.difficulty" 
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option :value="null">Selecione o nível de dificuldade</option>
                <option value="BEGINNER">Iniciante</option>
                <option value="INTERMEDIATE">Intermediário</option>
                <option value="ADVANCED">Avançado</option>
              </select>
            </div>
          </div>

          <!-- Excerpt -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Resumo *</label>
            <textarea 
              v-model="form.excerpt" 
              rows="3" 
              required
              placeholder="Escreva um breve resumo que desperte o interesse do leitor..."
              maxlength="300"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            ></textarea>
            <p class="text-xs text-gray-500 mt-1">{{ form.excerpt.length }}/300 caracteres</p>
          </div>
        </div>

        <!-- Featured Image -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Imagem de Capa</h2>
          
          <!-- Image Upload Method Selection -->
          <div class="mb-4">
            <div class="flex gap-4">
              <label class="flex items-center">
                <input 
                  type="radio" 
                  v-model="imageUploadMethod" 
                  value="upload" 
                  class="mr-2 text-blue-600 focus:ring-blue-500"
                >
                <span class="text-sm font-medium text-gray-700">Enviar do computador</span>
              </label>
              <label class="flex items-center">
                <input 
                  type="radio" 
                  v-model="imageUploadMethod" 
                  value="url" 
                  class="mr-2 text-blue-600 focus:ring-blue-500"
                >
                <span class="text-sm font-medium text-gray-700">Link da internet</span>
              </label>
            </div>
          </div>

          <div class="space-y-4">
            <div class="flex items-start gap-6">
              <!-- Image Preview -->
              <div class="w-48 h-32 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center bg-gray-50 relative overflow-hidden">
                <img v-if="form.cover_image" :src="form.cover_image" alt="Preview" class="w-full h-full object-cover rounded-lg">
                <div v-else class="text-center">
                  <ImageIcon class="h-8 w-8 text-gray-400 mx-auto mb-2" />
                  <span class="text-sm text-gray-500">Imagem de capa</span>
                </div>
                
                <!-- Remove Image Button -->
                <button 
                  v-if="form.cover_image" 
                  @click="removeImage" 
                  type="button"
                  class="absolute top-2 right-2 p-1 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
                >
                  <X class="h-3 w-3" />
                </button>
              </div>
              
              <!-- Upload Controls -->
              <div class="flex-1">
                <!-- File Upload -->
                <div v-if="imageUploadMethod === 'upload'" class="space-y-3">
                  <div>
                    <input 
                      ref="fileInput"
                      type="file" 
                      accept=".jpg,.jpeg,.png,.gif,image/jpeg,image/png,image/gif"
                      @change="handleFileUpload"
                      class="hidden"
                    >
                    <button 
                      @click="$refs.fileInput.click()" 
                      type="button"
                      class="w-full px-4 py-3 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-colors flex items-center justify-center gap-2"
                    >
                      <Upload class="h-5 w-5 text-gray-400" />
                      <span class="text-gray-600">Clique para selecionar uma imagem</span>
                    </button>
                  </div>
                  
                  <!-- Upload Progress -->
                  <div v-if="uploadProgress > 0 && uploadProgress < 100" class="space-y-2">
                    <div class="flex justify-between text-sm text-gray-600">
                      <span>Enviando...</span>
                      <span>{{ uploadProgress }}%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div class="bg-blue-600 h-2 rounded-full transition-all duration-300" :style="{ width: uploadProgress + '%' }"></div>
                    </div>
                  </div>
                  
                  <p class="text-sm text-gray-600">
                    Formatos aceitos: JPG, PNG, GIF (máx. 5MB)
                  </p>
                </div>

                <!-- URL Input -->
                <div v-else class="space-y-3">
                  <input 
                    type="url" 
                    v-model="form.cover_link" 
                    @input="handleUrlInput"
                    placeholder="Cole a URL da imagem aqui"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                  <p class="text-sm text-gray-600">
                    Cole o link direto de uma imagem da internet
                  </p>
                </div>
                
                <!-- Image Info -->
                <div v-if="imageInfo" class="mt-3 p-3 bg-gray-50 rounded-lg">
                  <div class="text-sm text-gray-600 space-y-1">
                    <div v-if="imageInfo.name">
                      <strong>Nome:</strong> {{ imageInfo.name }}
                    </div>
                    <div v-if="imageInfo.size">
                      <strong>Tamanho:</strong> {{ formatFileSize(imageInfo.size) }}
                    </div>
                    <div v-if="imageInfo.dimensions">
                      <strong>Dimensões:</strong> {{ imageInfo.dimensions }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Recommendations -->
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <h4 class="text-sm font-medium text-blue-900 mb-2">💡 Dicas para uma boa imagem de capa:</h4>
              <ul class="text-sm text-blue-800 space-y-1">
                <li>• Use proporção 16:9 (ex: 1600x900px) para melhor visualização</li>
                <li>• Resolução mínima recomendada: 800x450px</li>
                <li>• Evite imagens com muito texto</li>
                <li>• Prefira imagens relacionadas ao conteúdo do artigo</li>
              </ul>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Conteúdo do Artigo *</h2>
          <div class="flex justify-center">
            <div class="w-full max-w-5xl">
              <RichTextEditor v-model="form.content" />
            </div>
          </div>
          <div class="mt-2 text-sm text-gray-500">
            Palavras: {{ wordCount }} | Caracteres: {{ form.content.length }}
          </div>
        </div>

        <!-- Submit Actions -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex items-center justify-between">
            <div class="text-sm text-gray-600">
              <p>Seu artigo será revisado antes da publicação</p>
            </div>
            
            <div class="flex gap-3">
              <button type="button" @click="goBack" class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors">
                Cancelar
              </button>
              <button type="submit" class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                {{ isEditing ? 'Atualizar Artigo' : 'Publicar Artigo' }}
              </button>
            </div>
          </div>
        </div>
      </form>
    </div>

    <!-- Preview Modal -->
    <div v-if="showPreview" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg w-full max-w-4xl mx-4 max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200 flex justify-between items-center">
          <h3 class="text-lg font-semibold">Visualização do Artigo</h3>
          <button @click="showPreview = false" class="text-gray-400 hover:text-gray-600">
            <X class="h-6 w-6" />
          </button>
        </div>
        <div class="p-6">
          <img v-if="form.cover_image" :src="form.cover_image" :alt="form.title" class="w-full h-64 object-cover rounded-lg mb-6">
          <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ form.title }}</h1>
          <p class="text-xl text-gray-600 mb-6">{{ form.excerpt }}</p>
          <div class="prose max-w-none" v-html="form.content"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import articleService from '@/services/articleService';
import RichTextEditor from '@/components/RichTextEditor.vue';
import { 
  ArrowLeft, 
  Save, 
  Eye, 
  X, 
  Plus,
  Image as ImageIcon,
  Upload
} from 'lucide-vue-next'

const isEditing = computed(() => route.params.id !== undefined);
const imageFile = ref(null);
const categories = ref([]);

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

const form = ref({
  title: '',
  category: null, // Usaremos o ID da categoria
  excerpt: '', // Campo para o resumo do artigo
  content: '', // Inicializando com string vazia ao invés de undefined
  reading_time: 5, // Nome corrigido
  difficulty: 'BEGINNER', // Valor padrão corrigido
  cover_image: '', // Usado para preview
  cover_link: '',
});

const wordCount = computed(() => {
  return form.value.content.replace(/<[^>]*>/g, '').split(/\s+/).filter(word => word.length > 0).length
})

const handleSave = async (asDraft = false) => {
  isLoading.value = true;
  error.value = null;

  const formData = new FormData();

  // Mapeia os campos do formulário para os nomes esperados pelo backend
  formData.append('title', form.value.title);
  formData.append('category', form.value.category);
  formData.append('short_description', form.value.excerpt);
  formData.append('content', form.value.content);
  formData.append('reading_time', form.value.reading_time);
  formData.append('difficulty', form.value.difficulty);
  formData.append('cover_link', form.value.cover_link);
  
  // Define o status do artigo
  formData.append('is_draft', asDraft);
  formData.append('is_published', !asDraft);

  // Anexa o arquivo de imagem de capa, se houver um novo
  if (imageFile.value) {
    formData.append('cover_image', imageFile.value);
  }

  try {
    if (isEditing.value) {
      await articleService.updateArticle(route.params.id, formData);
    } else {
      await articleService.createArticle(formData);
    }
    // Redireciona para a lista de artigos após sucesso
    router.push('/articles'); 
  } catch (err) {
    console.error("Erro ao salvar artigo:", err.response?.data || err);
    error.value = "Falha ao salvar o artigo. Verifique os campos e tente novamente.";
    // Opcional: formatar o erro vindo da API para ser mais específico
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
    // Validate URL format
    try {
      new URL(form.value.cover_link)
      form.value.cover_image = form.value.cover_link
      
      // Try to get image dimensions
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
  // CORREÇÃO: O botão "Salvar Rascunho" agora chama a API com asDraft = true
  handleSave(true);
};

const previewArticle = () => {
  updateContent()
  showPreview.value = true
}

const handleSubmit = () => {
  // O botão principal "Publicar" chama o salvamento com asDraft = false
  handleSave(false);
};

onMounted(async () => {
  // Busca categorias para o dropdown
  try {
    const response = await articleService.getCategories();
    categories.value = response.data;
  } catch (err) {
    console.error('Erro ao carregar categorias:', err);
  }

  // Se estiver editando, busca os dados do artigo
  if (isEditing.value) {
    try {
      const response = await articleService.getArticleDetail(route.params.id);
      const articleData = response.data;
      
      // Preenche o formulário com os dados da API
      form.value.title = articleData.title;
      form.value.category = articleData.category; // Assumindo que a API retorna o ID
      form.value.excerpt = articleData.excerpt;
      form.value.content = articleData.content;
      form.value.reading_time = articleData.reading_time;
      form.value.difficulty = articleData.difficulty;
      form.value.cover_image = articleData.cover_image; // URL da imagem existente para preview
      form.value.cover_link = articleData.cover_link;
      
    } catch (err) {
      console.error('Erro ao carregar artigo para edição:', err);
      // Opcional: redirecionar ou mostrar erro
    }
  }
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