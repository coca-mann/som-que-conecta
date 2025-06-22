<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto px-0 sm:px-6 lg:px-8 py-12">
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
          v-if="isAuthenticated"
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
              :disabled="isAuthenticated"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent bg-gray-100 cursor-not-allowed"
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
              :disabled="isAuthenticated"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent bg-gray-100 cursor-not-allowed"
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
                accept="image/jpeg, image/png, image/gif, application/pdf, .doc, .docx, .txt"
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

        <div
          v-else
          class="text-center"
        >
          <h3 class="text-lg font-semibold text-gray-800 mb-3">
            Acesso Restrito
          </h3>
          <p class="text-gray-600 mb-6">
            Para enviar uma solicitação de ajuda, por favor, faça login na sua conta.
          </p>
          <router-link
            to="/auth"
            class="inline-block px-8 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors font-medium"
          >
            Fazer Login ou Registrar-se
          </router-link>
        </div>
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
        class="fixed inset-0 flex items-center justify-center z-50"
      >
        <!-- Backdrop embaçado -->
        <div class="absolute inset-0 bg-white/30 backdrop-blur-sm" />
        <div class="bg-white rounded-lg border border-gray-200 w-full max-w-md mx-4 p-6 relative z-10">
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
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.store'; // 1. Importe o authStore
import { storeToRefs } from 'pinia';
import { Paperclip, X, Send, Loader2, ChevronDown, CheckCircle } from 'lucide-vue-next'
import { useHead } from '@vueuse/head';

useHead({
  title: 'Central de Ajuda | Som que Conecta',
  meta: [
    { name: 'description', content: 'Solicite ajuda sobre qualquer situação na plataforma Som que Conecta.' },
  ]
})

const authStore = useAuthStore();
// 3. Pega o status de login e os dados do usuário de forma reativa
const { isAuthenticated, user } = storeToRefs(authStore);


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
  // Mantive as suas duas perguntas originais
  {
    question: 'Como posso recuperar minha senha?',
    answer: 'Para recuperar sua senha, clique no link "Esqueceu a senha?" na tela de login. Você receberá um e-mail com as instruções para criar uma nova senha de acesso.'
  },
  {
    question: 'O uso da plataforma e dos minicursos é realmente gratuito?',
    answer: 'Sim! Nossa missão é democratizar o acesso à educação musical. Todo o conteúdo, incluindo minicursos e artigos, é 100% gratuito. A plataforma é mantida através de parcerias e doações.'
  },
  {
    question: 'Como funciona o sistema de empréstimo de instrumentos?',
    answer: 'Nós conectamos pessoas que querem aprender com ONGs e professores que disponibilizam instrumentos. Você pode navegar pelos instrumentos disponíveis e solicitar um agendamento para avaliação. A negociação e a retirada do instrumento são feitas diretamente com o responsável (ONG ou professor), e a nossa plataforma serve como a ponte para essa conexão.'
  },
  {
    question: 'Eu tenho um instrumento parado. Como posso disponibilizá-lo para empréstimo?',
    answer: 'Ficamos muito felizes com seu interesse! Para garantir a segurança e a qualidade do programa, apenas usuários com o perfil de "Professor" ou "ONG" podem cadastrar instrumentos. Você pode solicitar a mudança do seu perfil enviando uma mensagem pelo formulário dessa página, e nossa equipe analisará seu pedido.'
  },
  {
    question: 'Como meu progresso nos minicursos é calculado?',
    answer: 'Seu progresso é calculado com base no número de tarefas que você marca como "concluída" dentro de cada minicurso. Ao completar a primeira tarefa, você é automaticamente "matriculado", e a barra de progresso passará a refletir sua evolução.'
  },
  {
    question: 'Quem pode escrever artigos na plataforma?',
    answer: 'A criação de artigos é reservada para nossos parceiros e usuários com perfil de "Professor" ou "ONG". Isso nos ajuda a manter um alto nível de qualidade e confiabilidade no conteúdo oferecido. Todos os artigos passam por uma moderação automática antes de serem publicados.'
  }
];

onMounted(() => {
  if (isAuthenticated.value && user.value) {
    form.value.name = `${user.value.first_name || ''} ${user.value.last_name || ''}`.trim();
    form.value.email = user.value.email;
  }
});


const handleFileAttachment = (event) => {
  const file = event.target.files[0]
  if (!file) return

  // ATUALIZE ESTA LISTA DE TIPOS PERMITIDOS
  const allowedTypes = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'application/pdf',
    'application/msword', // para .doc
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // para .docx
    'text/plain' // para .txt
  ]

  if (!allowedTypes.includes(file.type)) {
    // A mensagem de alerta agora é mais completa
    alert('Tipo de arquivo inválido. Por favor, selecione apenas imagens (JPG, PNG, GIF), PDF, documentos Word (.doc, .docx) ou arquivos de texto (.txt).')
    // Limpa a seleção de arquivo inválido
    if (fileInput.value) {
      fileInput.value.value = ''
    }
    return
  }

  // A validação de tamanho continua a mesma
  if (file.size > 5 * 1024 * 1024) { // 5MB max
    alert('O arquivo deve ter no máximo 5MB.')
    if (fileInput.value) {
      fileInput.value.value = ''
    }
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

const subjectOptions = {
  account: 'Conta e Perfil',
  courses: 'Cursos e Conteúdo',
  technical: 'Problemas Técnicos',
  feedback: 'Sugestões e Feedback',
  other: 'Outro Assunto'
};

const submitHelpRequest = async () => {
  isSubmitting.value = true;
  
  // Usamos FormData por causa do anexo de arquivo
  const formData = new FormData();
  formData.append('name', form.value.name);
  formData.append('email', form.value.email);
  // Envia o texto da opção selecionada, não a chave
  const subjectText = subjectOptions[form.value.subject] || '';
  formData.append('subject', subjectText);
  formData.append('message', form.value.message);
  
  if (form.value.attachment) {
    formData.append('attachment', form.value.attachment);
  }

  try {
    await authStore.sendHelpRequest(formData); // Supondo que você adicione a action no store
    
    // Limpa o formulário e mostra o modal de sucesso
    form.value = { name: authStore.user.name, email: authStore.user.email, subject: '', message: '', attachment: null };
    showSuccessModal.value = true;

  } catch (error) {
    console.error('Erro ao enviar mensagem:', error.response?.data || error);
    alert('Houve um erro ao enviar sua mensagem. Tente novamente.');
  } finally {
    isSubmitting.value = false;
  }
};

</script>