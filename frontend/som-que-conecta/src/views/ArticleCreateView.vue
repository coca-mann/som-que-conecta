<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
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
                <option value="">Selecione uma categoria</option>
                <option value="Teoria">Teoria Musical</option>
                <option value="Prática">Prática</option>
                <option value="Instrumentos">Instrumentos</option>
                <option value="História">História da Música</option>
                <option value="Iniciantes">Iniciantes</option>
                <option value="Avançado">Avançado</option>
              </select>
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Tempo de Leitura</label>
              <input 
                v-model.number="form.readTime" 
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
                <option value="iniciante">Iniciante</option>
                <option value="intermediario">Intermediário</option>
                <option value="avancado">Avançado</option>
              </select>
            </div>
          </div>

          <!-- Tags -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">Tags</label>
            <div class="flex flex-wrap gap-2 mb-2">
              <span v-for="tag in form.tags" :key="tag" class="inline-flex items-center gap-1 px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full">
                {{ tag }}
                <button @click="removeTag(tag)" type="button" class="text-blue-600 hover:text-blue-800">
                  <X class="h-3 w-3" />
                </button>
              </span>
            </div>
            <div class="flex gap-2">
              <input 
                v-model="newTag" 
                @keydown.enter.prevent="addTag"
                type="text" 
                placeholder="Digite uma tag e pressione Enter"
                class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
              <button @click="addTag" type="button" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                <Plus class="h-4 w-4" />
              </button>
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
                <img v-if="form.image" :src="form.image" alt="Preview" class="w-full h-full object-cover rounded-lg">
                <div v-else class="text-center">
                  <ImageIcon class="h-8 w-8 text-gray-400 mx-auto mb-2" />
                  <span class="text-sm text-gray-500">Imagem de capa</span>
                </div>
                
                <!-- Remove Image Button -->
                <button 
                  v-if="form.image" 
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
                    v-model="form.imageUrl" 
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

        <!-- Rich Text Editor -->
        <div class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Conteúdo do Artigo *</h2>
          
          <!-- Editor Toolbar -->
          <div class="border border-gray-300 rounded-t-lg p-3 bg-gray-50 flex flex-wrap gap-2">
            <div class="flex items-center gap-1 border-r border-gray-300 pr-2 mr-2">
              <button @click="formatText('bold')" type="button" :class="['p-2 rounded hover:bg-gray-200 transition-colors', isActive('bold') ? 'bg-gray-300' : '']">
                <Bold class="h-4 w-4" />
              </button>
              <button @click="formatText('italic')" type="button" :class="['p-2 rounded hover:bg-gray-200 transition-colors', isActive('italic') ? 'bg-gray-300' : '']">
                <Italic class="h-4 w-4" />
              </button>
              <button @click="formatText('underline')" type="button" :class="['p-2 rounded hover:bg-gray-200 transition-colors', isActive('underline') ? 'bg-gray-300' : '']">
                <Underline class="h-4 w-4" />
              </button>
            </div>
            
            <div class="flex items-center gap-1 border-r border-gray-300 pr-2 mr-2">
              <select @change="formatHeading($event)" class="px-2 py-1 border border-gray-300 rounded text-sm">
                <option value="">Parágrafo</option>
                <option value="h1">Título 1</option>
                <option value="h2">Título 2</option>
                <option value="h3">Título 3</option>
              </select>
            </div>
            
            <div class="flex items-center gap-1 border-r border-gray-300 pr-2 mr-2">
              <button @click="formatText('insertUnorderedList')" type="button" class="p-2 rounded hover:bg-gray-200 transition-colors">
                <List class="h-4 w-4" />
              </button>
              <button @click="formatText('insertOrderedList')" type="button" class="p-2 rounded hover:bg-gray-200 transition-colors">
                <ListOrdered class="h-4 w-4" />
              </button>
            </div>
            
            <div class="flex items-center gap-1">
              <button @click="insertLink" type="button" class="p-2 rounded hover:bg-gray-200 transition-colors">
                <LinkIcon class="h-4 w-4" />
              </button>
              <button @click="insertImage" type="button" class="p-2 rounded hover:bg-gray-200 transition-colors">
                <ImageIcon class="h-4 w-4" />
              </button>
            </div>
          </div>
          
          <!-- Editor Content -->
          <div 
            ref="editor"
            contenteditable="true"
            @input="updateContent"
            @keydown="handleKeydown"
            class="min-h-[400px] p-4 border border-gray-300 border-t-0 rounded-b-lg focus:outline-none focus:ring-2 focus:ring-blue-500 prose max-w-none"
            style="white-space: pre-wrap;"
            placeholder="Comece a escrever seu artigo aqui..."
          ></div>
          
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
          <img v-if="form.image" :src="form.image" :alt="form.title" class="w-full h-64 object-cover rounded-lg mb-6">
          <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ form.title }}</h1>
          <p class="text-xl text-gray-600 mb-6">{{ form.excerpt }}</p>
          <div class="prose max-w-none" v-html="form.content"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import articleService from '@/services/articleService';
import { 
  ArrowLeft, 
  Save, 
  Eye, 
  X, 
  Plus, 
  Bold, 
  Italic, 
  Underline, 
  List, 
  ListOrdered, 
  Link as LinkIcon, 
  Image as ImageIcon,
  Upload
} from 'lucide-vue-next'

const isEditing = computed(() => route.params.id !== undefined);
const imageFile = ref(null);

const router = useRouter()
const route = useRoute()
const editor = ref(null)
const fileInput = ref(null)
const showPreview = ref(false)
const newTag = ref('')
const imageUploadMethod = ref('upload')
const uploadProgress = ref(0)
const imageInfo = ref(null)

const form = ref({
  title: '',
  category: '',
  excerpt: '',
  content: '',
  readTime: 5,
  difficulty: 'iniciante',
  image: '',
  imageUrl: '',
  tags: [],
  author: 'Usuário Atual' // Should come from auth store
})

const wordCount = computed(() => {
  return form.value.content.replace(/<[^>]*>/g, '').split(/\s+/).filter(word => word.length > 0).length
})

const goBack = () => {
  router.push('/articles')
}

const updateContent = () => {
  if (editor.value) {
    form.value.content = editor.value.innerHTML
  }
}

const formatText = (command, value = null) => {
  document.execCommand(command, false, value)
  editor.value.focus()
}

const formatHeading = (event) => {
  const tag = event.target.value
  if (tag) {
    formatText('formatBlock', tag)
  }
  event.target.value = ''
}

const isActive = (command) => {
  return document.queryCommandState(command)
}

const insertLink = () => {
  const url = prompt('Digite a URL do link:')
  if (url) {
    formatText('createLink', url)
  }
}

const insertImage = () => {
  const url = prompt('Digite a URL da imagem:')
  if (url) {
    formatText('insertImage', url)
  }
}

const addTag = () => {
  if (newTag.value.trim() && !form.value.tags.includes(newTag.value.trim())) {
    form.value.tags.push(newTag.value.trim())
    newTag.value = ''
  }
}

const removeTag = (tag) => {
  const index = form.value.tags.indexOf(tag)
  if (index > -1) {
    form.value.tags.splice(index, 1)
  }
}

const handleKeydown = (event) => {
  // Handle tab key for indentation
  if (event.key === 'Tab') {
    event.preventDefault()
    formatText('insertHTML', '&nbsp;&nbsp;&nbsp;&nbsp;')
  }
}

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;
    form.value.image = URL.createObjectURL(file); // Para preview
  }
};

const handleUrlInput = () => {
  if (form.value.imageUrl) {
    // Validate URL format
    try {
      new URL(form.value.imageUrl)
      form.value.image = form.value.imageUrl
      
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
      img.src = form.value.imageUrl
    } catch (error) {
      form.value.image = ''
      imageInfo.value = null
    }
  } else {
    form.value.image = ''
    imageInfo.value = null
  }
}

const removeImage = () => {
  form.value.image = ''
  form.value.imageUrl = ''
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
  // Save to localStorage or send to backend
  localStorage.setItem('articleDraft', JSON.stringify(form.value))
  console.log('Draft saved')
}

const previewArticle = () => {
  updateContent()
  showPreview.value = true
}

const handleSubmit = async () => {
  const formData = new FormData();
  
  // Adiciona todos os campos do formulário ao FormData
  Object.keys(form.value).forEach(key => {
    if (key !== 'image') { // Não envie a URL de preview
      formData.append(key, form.value[key]);
    }
  });

  // Se uma nova imagem foi selecionada, adicione o arquivo
  if (imageFile.value) {
    formData.append('cover_image', imageFile.value);
  } else if (!form.value.image) {
    // Se a imagem foi removida, envie um valor vazio
    formData.append('cover_image', '');
  }
  
  try {
    if (isEditing.value) {
      await articleService.updateArticle(route.params.id, formData);
    } else {
      await articleService.createArticle(formData);
    }
    router.push('/articles'); // Redireciona para a lista
  } catch (error) {
    console.error("Erro ao salvar artigo:", error);
    alert("Falha ao salvar o artigo.");
  }
};

onMounted(() => {
  if (isEditing.value) {
    articleService.getArticleDetail(route.params.id).then(response => {
      // Preenche o formulário com os dados da API
      Object.assign(form.value, response.data);
      form.value.image = response.data.cover_image; // URL da imagem existente
    });
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

[contenteditable]:empty:before {
  content: attr(placeholder);
  color: #9CA3AF;
  font-style: italic;
}
</style>