<template>
  <div class="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-2xl mx-4 max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-900">
          {{ instrument ? 'Editar Instrumento' : 'Adicionar Instrumento' }}
        </h2>
        <button
          class="text-gray-400 hover:text-red-600 transition-colors"
          @click="$emit('close')"
        >
          <X class="h-6 w-6" />
        </button>
      </div>
      
      <form
        class="space-y-6"
        @submit.prevent="handleSubmit"
      >
        <div class="pt-4 border-t">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Fotos (máximo 5 imagens)
          </label>
          
          <p
            v-if="existingImages.length === 0 && newImagePreviews.length === 0" 
            class="text-sm text-gray-500 mb-4"
          >
            Nenhuma foto adicionada.
          </p>
          
          <div
            v-if="existingImages.length > 0"
            class="grid grid-cols-3 sm:grid-cols-5 gap-4 mb-4"
          >
            <div
              v-for="image in existingImages"
              :key="image.id"
              class="relative group"
            >
              <img
                :src="image.picture"
                :alt="'Foto do instrumento ' + image.id" 
                class="w-full h-24 object-cover rounded-md border"
              >
              <button 
                type="button" 
                class="absolute top-1 right-1 bg-red-600 text-white rounded-full p-1 opacity-50 group-hover:opacity-100 transition-opacity"
                title="Marcar para excluir"
                @click="markImageForDeletion(image.id)"
              >
                <Trash2 class="h-3 w-3" />
              </button>
            </div>
          </div>
          
          <div
            v-if="newImagePreviews.length > 0"
            class="grid grid-cols-3 sm:grid-cols-5 gap-4 mb-4"
          >
            <div
              v-for="(preview, index) in newImagePreviews"
              :key="index"
              class="relative group"
            >
              <img
                :src="preview"
                alt="Preview da nova foto" 
                class="w-full h-24 object-cover rounded-md border-2 border-dashed border-green-400"
              >
              <button 
                type="button" 
                class="absolute top-1 right-1 bg-red-600 text-white rounded-full p-1 opacity-50 group-hover:opacity-100 transition-opacity"
                title="Remover anexo"
                @click="removeNewFile(index)"
              >
                <X class="h-3 w-3" />
              </button>
            </div>
          </div>

          <div v-if="totalImages < 5">
            <label
              for="file-upload" 
              class="relative cursor-pointer bg-white rounded-md font-medium text-red-600 hover:text-red-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-red-500 border-2 border-gray-300 border-dashed px-4 py-6 flex flex-col items-center justify-center text-center transition-colors"
            >
              <UploadCloud class="h-8 w-8 text-gray-400 mb-2" />
              <span>Adicionar fotos ({{ totalImages }}/5)</span>
              <input
                id="file-upload"
                name="file-upload"
                type="file"
                class="sr-only" 
                multiple
                accept="image/*"
                @change="handleFileChange"
              >
            </label>
          </div>
          
          <p
            v-else
            class="text-sm text-amber-600 bg-amber-50 p-2 rounded-md"
          >
            Limite máximo de 5 imagens atingido.
          </p>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Nome do Instrumento *</label>
          <input
            v-model="form.name"
            type="text"
            required 
            placeholder="Ex: Violão Clássico Yamaha C40" 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
          >
        </div>

        <div class="grid md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Marca *</label>
            <select 
              v-model="form.brand_name" 
              required 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            >
              <option disabled value="">Selecione a marca</option>
              <option v-for="brand in instrumentBrands" :key="brand.id" :value="brand.name">{{ brand.name }}</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Tipo *</label>
            <select 
              v-model="form.type_name" 
              required 
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            >
              <option disabled value="">Selecione o tipo</option>
              <option v-for="type in instrumentTypes" :key="type.id" :value="type.name">{{ type.name }}</option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
          <textarea 
            v-model="form.description" 
            rows="4" 
            placeholder="Descreva as características, condições e especificações do instrumento..."
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent resize-none"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Status *</label>
          <select 
            v-model="form.is_active" 
            required 
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
          >
            <option :value="true">ATIVO</option>
            <option :value="false">INATIVO</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Cor do Instrumento</label>
          <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
            <div
              v-for="colorOption in predefinedColors"
              :key="colorOption.name"
              :class="[
                'flex items-center gap-2 p-3 border-2 rounded-lg cursor-pointer transition-all',
                form.color_name === colorOption.name 
                  ? 'border-red-500 bg-red-50' 
                  : 'border-gray-200 hover:border-gray-300'
              ]"
              @click="selectColor(colorOption)"
            >
              <div
                :style="{ backgroundColor: colorOption.hex }" 
                class="w-6 h-6 rounded-full border border-gray-300 shadow-sm"
              />
              <span class="text-sm font-medium">{{ colorOption.name }}</span>
            </div>
          </div>
        </div>

        <div
          v-if="props.showDetailedFields"
          class="grid md:grid-cols-2 gap-4"
        >
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Localização</label>
            <input 
              v-model="form.location" 
              type="text" 
              placeholder="Rua A, 12 - Sala 15, Bairro Zona Leste, Porto Velho - RO"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            >
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Disponibilidade</label>
            <input 
              v-model="form.availability" 
              type="text" 
              placeholder="Seg a Sex, 08hrs às 18hrs"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            >
          </div>
        </div>

        <div class="flex justify-end gap-3 pt-4 border-t">
          <button
            type="button"
            class="px-6 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors" 
            @click="$emit('close')"
          >
            Cancelar
          </button>
          <button
            type="submit" 
            class="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            {{ instrument ? 'Atualizar' : 'Adicionar' }} Instrumento
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue';
import { X, UploadCloud, Trash2 } from 'lucide-vue-next';
import instrumentService from '@/services/instrumentService';
import { useAuthStore } from '@/stores/auth.store';

const props = defineProps({
  instrument: {
    type: Object,
    default: null
  },
  showDetailedFields: { // <-- Nova prop recebida do pai
    type: Boolean,
    default: false
  }
});


const emit = defineEmits(['close', 'saved']);
const authStore = useAuthStore();

// Estado do Formulário
const form = ref({
  name: '',
  brand_name: '',
  type_name: '',
  description: '',
  is_active: true,
  color: '',
  color_name: '',
  location: '',
  availability: ''
});

// Estados para Gerenciar Fotos
const existingImages = ref([]);
const newFiles = ref([]);
const newImagePreviews = ref([]);
const picturesToDelete = ref([]);

// Computed para controlar o total de imagens
const totalImages = computed(() => {
  return existingImages.value.length + newImagePreviews.value.length;
});

// Dados para os selects
const instrumentTypes = ref([]);
const instrumentBrands = ref([]);

// Cores pré-definidas para instrumentos musicais
const predefinedColors = ref([
  { name: 'Natural', hex: '#D2B48C', color: 'natural' },
  { name: 'Preto', hex: '#000000', color: 'black' },
  { name: 'Branco', hex: '#FFFFFF', color: 'white' },
  { name: 'Marrom', hex: '#8B4513', color: 'brown' },
  { name: 'Vermelho', hex: '#DC143C', color: 'red' },
  { name: 'Azul', hex: '#4169E1', color: 'blue' },
  { name: 'Verde', hex: '#228B22', color: 'green' },
  { name: 'Amarelo', hex: '#FFD700', color: 'yellow' },
  { name: 'Laranja', hex: '#FF8C00', color: 'orange' },
  { name: 'Roxo', hex: '#8A2BE2', color: 'purple' },
  { name: 'Rosa', hex: '#FF69B4', color: 'pink' },
  { name: 'Dourado', hex: '#FFD700', color: 'gold' },
  { name: 'Prateado', hex: '#C0C0C0', color: 'silver' },
  { name: 'Bronze', hex: '#CD7F32', color: 'bronze' },
  { name: 'Mogno', hex: '#C04000', color: 'mahogany' },
  { name: 'Cerejeira', hex: '#DE3163', color: 'cherry' }
]);

// Função para selecionar cor
const selectColor = (colorOption) => {
  form.value.color = colorOption.hex;
  form.value.color_name = colorOption.name;
};

// Carregar dados do formulário
const loadFormDependencies = async () => {
  try {
    const [typesResponse, brandsResponse] = await Promise.all([
      instrumentService.getInstrumentTypes(),
      instrumentService.getInstrumentBrands(),
    ]);
    instrumentTypes.value = typesResponse.data;
    instrumentBrands.value = brandsResponse.data;
  } catch (error) {
    console.error("Erro ao carregar dados do formulário:", error);
  }
};

onMounted(() => {
  loadFormDependencies();
});

// Watch para preencher o formulário no modo de edição
watch(() => props.instrument, (newVal) => {
  if (newVal) {
    form.value.name = newVal.name || '';
    form.value.brand_name = newVal.brand_name || '';
    form.value.type_name = newVal.type_name || '';
    form.value.description = newVal.description || '';
    form.value.is_active = newVal.is_active !== undefined ? newVal.is_active : true;
    form.value.color = newVal.color || '';
    form.value.color_name = newVal.color_name || '';
    form.value.location = newVal.location || '';
    form.value.availability = newVal.availability || '';

    existingImages.value = newVal.images ? [...newVal.images] : [];
    newFiles.value = [];
    newImagePreviews.value = [];
    picturesToDelete.value = [];
  } else {
    // Reset do formulário
    form.value = {
      name: '',
      brand_name: '',
      type_name: '',
      description: '',
      is_active: true,
      color: '',
      color_name: '',
      location: '',
      availability: ''
    };
    existingImages.value = [];
    newFiles.value = [];
    newImagePreviews.value = [];
    picturesToDelete.value = [];
  }
}, { immediate: true, deep: true });

// Manipulação de arquivos
const handleFileChange = (event) => {
  const files = Array.from(event.target.files);
  if (!files.length) return;

  // Verificar se não excede o limite de 5 imagens
  const remainingSlots = 5 - totalImages.value;
  const filesToAdd = files.slice(0, remainingSlots);

  if (filesToAdd.length < files.length) {
    alert(`Apenas ${filesToAdd.length} imagem(ns) foi(ram) adicionada(s). Limite máximo de 5 imagens.`);
  }

  newFiles.value.push(...filesToAdd);

  for (const file of filesToAdd) {
    newImagePreviews.value.push(URL.createObjectURL(file));
  }

  // Limpar o input
  event.target.value = '';
};

const removeNewFile = (index) => {
  // Revogar a URL do objeto para liberar memória
  URL.revokeObjectURL(newImagePreviews.value[index]);
  newFiles.value.splice(index, 1);
  newImagePreviews.value.splice(index, 1);
};

const markImageForDeletion = (imageId) => {
  picturesToDelete.value.push(imageId);
  existingImages.value = existingImages.value.filter(img => img.id !== imageId);
};

// Função para salvar
const handleSubmit = async () => {
  const formData = new FormData();

  // Adicionar campos do formulário
  Object.keys(form.value).forEach(key => {
    const value = form.value[key];
    if (value !== null && value !== '') {
      formData.append(key, value);
    }
  });

  // Adicionar novos arquivos de imagem
  newFiles.value.forEach(file => {
    formData.append('new_pictures', file);
  });

  // Adicionar lista de IDs para deletar
  if (picturesToDelete.value.length > 0) {
    formData.append('images_to_delete', JSON.stringify(picturesToDelete.value));
  }
  
  try {
    if (props.instrument && props.instrument.id) {
      await instrumentService.updateInstrument(props.instrument.id, formData);
    } else {
      await instrumentService.createInstrument(formData);
    }
    emit('saved');
    emit('close');
  } catch (error) {
    console.error("Erro ao salvar instrumento:", error.response?.data || error);
    alert("Ocorreu um erro ao salvar. Verifique o console para mais detalhes.");
  }
};
</script>
