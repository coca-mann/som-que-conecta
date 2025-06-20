<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="text-center mb-10">
        <h1 class="text-3xl font-bold text-gray-900 mb-3">
          Central de Ajuda
        </h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto">
          Estamos aqui para ajudar. Preencha o formulário abaixo e nossa equipe entrará em contato o mais breve possível.
        </p>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-8">
        <form
          class="space-y-6"
          @submit.prevent="submitHelpRequest"
        >
          <div>
            <label
              for="name"
              class="block text-sm font-medium text-gray-700 mb-2"
            >Nome completo</label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              placeholder="Digite seu nome completo"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            >
          </div>

          <div>
            <label
              for="email"
              class="block text-sm font-medium text-gray-700 mb-2"
            >Email de contato</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              placeholder="seu.email@exemplo.com"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            >
          </div>

          <div>
            <label
              for="subject"
              class="block text-sm font-medium text-gray-700 mb-2"
            >Assunto</label>
            <select
              id="subject"
              v-model="form.subject"
              required
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            >
              <option value="">
                Selecione um assunto
              </option>
              <option value="account">
                Conta e Perfil
              </option>
              <option value="courses">
                Cursos e Conteúdo
              </option>
              <option value="payment">
                Pagamentos
              </option>
              <option value="technical">
                Problemas Técnicos
              </option>
              <option value="feedback">
                Sugestões e Feedback
              </option>
              <option value="other">
                Outro Assunto
              </option>
            </select>
          </div>

          <div>
            <label
              for="message"
              class="block text-sm font-medium text-gray-700 mb-2"
            >Mensagem</label>
            <textarea
              id="message"
              v-model="form.message"
              rows="6"
              required
              placeholder="Descreva detalhadamente como podemos ajudar..."
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent resize-none"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Anexo (opcional)</label>
            <div class="flex items-center">
              <input
                ref="fileInput"
                type="file"
                class="hidden"
                @change="handleFileAttachment"
              >
              <button
                type="button"
                class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors flex items-center gap-2"
                @click="$refs.fileInput.click()"
              >
                <Paperclip class="h-4 w-4" />
                Anexar arquivo
              </button>
              <span
                v-if="form.attachment"
                class="ml-3 text-sm text-gray-600"
              >
                {{ form.attachment.name }} ({{ formatFileSize(form.attachment.size) }})
                <button 
                  type="button" 
                  class="ml-2 text-red-600 hover:text-red-800" 
                  @click="removeAttachment"
                >
                  <X class="h-4 w-4 inline" />
                </button>
              </span>
            </div>
            <p class="text-xs text-gray-500 mt-2">
              Formatos aceitos: PDF, JPG, PNG (máx. 5MB)
            </p>
          </div>

          <div class="pt-4">
            <button
              type="submit"
              :disabled="isSubmitting"
              class="w-full px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center justify-center gap-2 disabled:opacity-70"
            >
              <Loader2
                v-if="isSubmitting"
                class="h-5 w-5 animate-spin"
              />
              <Send
                v-else
                class="h-5 w-5"
              />
              {{ isSubmitting ? 'Enviando...' : 'Enviar Mensagem' }}
            </button>
          </div>
        </form>
      </div>

      <div class="mt-12">
        <h2 class="text-2xl font-bold text-gray-900 mb-6">
          Perguntas Frequentes
        </h2>
        
        <div class="space-y-4">
          <div
            v-for="(faq, index) in faqs"
            :key="index"
            class="border border-gray-200 rounded-lg"
          >
            <button
              class="w-full px-6 py-4 flex items-center justify-between text-left focus:outline-none"
              @click="toggleFaq(index)"
            >
              <span class="font-medium text-gray-900">{{ faq.question }}</span>
              <ChevronDown
                :class="[
                  'h-5 w-5 text-gray-500 transition-transform',
                  openFaq === index ? 'transform rotate-180' : ''
                ]"
              />
            </button>
            <div
              v-if="openFaq === index"
              class="px-6 py-4 bg-gray-50 border-t border-gray-200"
            >
              <p class="text-gray-700">
                {{ faq.answer }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="showSuccessModal"
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      >
        <div class="bg-white rounded-lg w-full max-w-md mx-4 p-6">
          <div class="text-center">
            <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 mb-4">
              <CheckCircle class="h-6 w-6 text-green-600" />
            </div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">
              Mensagem Enviada!
            </h3>
            <p class="text-gray-600 mb-6">
              Obrigado por entrar em contato. Nossa equipe responderá em breve para o email fornecido.
            </p>
            <button
              class="w-full px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              @click="showSuccessModal = false"
            >
              Fechar
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Paperclip, X, Send, Loader2, ChevronDown, CheckCircle } from 'lucide-vue-next'
import { useHead } from '@vueuse/head';

useHead({
  title: 'Central de Ajuda | Som que Conecta',
  meta: [
    { name: 'description', content: 'Solicite ajuda sobre qualquer situação na plataforma Som que Conecta.' },
  ]
})

const form = ref({
  name: '',
  email: '',
  subject: '',
  message: '',
  attachment: null
})

const fileInput = ref(null)
const isSubmitting = ref(false)
const showSuccessModal = ref(false)
const openFaq = ref(null)

const faqs = [
  {
    question: 'Como posso recuperar minha senha?',
    answer: 'Para recuperar sua senha, clique em "Esqueci minha senha" na tela de login. Você receberá um email com instruções para criar uma nova senha.'
  },
  {
    question: 'Como cancelar minha assinatura?',
    answer: 'Você pode cancelar sua assinatura a qualquer momento acessando a seção "Assinaturas" em seu perfil. O cancelamento será efetivado ao final do período já pago.'
  },
  {
    question: 'Os certificados são reconhecidos oficialmente?',
    answer: 'Nossos certificados atestam a conclusão dos cursos em nossa plataforma. Embora não sejam diplomas oficiais, são reconhecidos no mercado como comprovação de desenvolvimento de habilidades.'
  },
  {
    question: 'Posso acessar os cursos offline?',
    answer: 'Sim! Você pode baixar as aulas para assistir offline através do nosso aplicativo móvel. O conteúdo ficará disponível por 30 dias para acesso sem internet.'
  },
  {
    question: 'Como faço para me tornar um instrutor?',
    answer: 'Para se tornar um instrutor, acesse a seção "Torne-se um Instrutor" em nosso site e preencha o formulário de candidatura. Nossa equipe analisará seu perfil e entrará em contato.'
  }
]

const handleFileAttachment = (event) => {
  const file = event.target.files[0]
  if (!file) return

  // Validate file type
  const allowedTypes = ['application/pdf', 'image/jpeg', 'image/png']
  if (!allowedTypes.includes(file.type)) {
    alert('Por favor, selecione apenas arquivos PDF, JPG ou PNG.')
    return
  }

  // Validate file size (5MB max)
  if (file.size > 5 * 1024 * 1024) {
    alert('O arquivo deve ter no máximo 5MB.')
    return
  }

  form.value.attachment = file
}

const removeAttachment = () => {
  form.value.attachment = null
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

const toggleFaq = (index) => {
  openFaq.value = openFaq.value === index ? null : index
}

const submitHelpRequest = async () => {
  isSubmitting.value = true
  
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1500))
  
  console.log('Help request submitted:', {
    ...form.value,
    attachment: form.value.attachment ? form.value.attachment.name : null
  })
  
  // Reset form
  form.value = {
    name: '',
    email: '',
    subject: '',
    message: '',
    attachment: null
  }
  
  isSubmitting.value = false
  showSuccessModal.value = true
}
</script>