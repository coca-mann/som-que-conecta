<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Header -->
      <div class="text-center mb-10">
        <h1 class="text-3xl font-bold text-gray-900 mb-3">Política de Privacidade</h1>
        <p class="text-gray-600">
          Última atualização: 5 de junho de 2024
        </p>
      </div>

      <!-- Table of Contents -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Índice</h2>
        <ul class="space-y-2">
          <li v-for="(section, index) in sections" :key="index">
            <a 
              :href="`#section-${index + 1}`" 
              class="text-blue-600 hover:text-blue-800 hover:underline flex items-center"
            >
              {{ index + 1 }}. {{ section.title }}
              <ChevronRight class="h-4 w-4 ml-1" />
            </a>
          </li>
        </ul>
      </div>

      <!-- Privacy Policy Content -->
      <div class="bg-white rounded-lg shadow-sm p-8">
        <div class="prose max-w-none">
          <p class="text-gray-700 mb-6">
            A Music Learning está comprometida em proteger sua privacidade. Esta Política de Privacidade explica como coletamos, usamos, divulgamos e protegemos suas informações pessoais quando você utiliza nossa plataforma e serviços.
          </p>

          <div v-for="(section, index) in sections" :key="index" :id="`section-${index + 1}`" class="mb-8">
            <h2 class="text-xl font-semibold text-gray-900 mb-4">{{ index + 1 }}. {{ section.title }}</h2>
            <div v-html="section.content"></div>
          </div>

          <h2 class="text-xl font-semibold text-gray-900 mb-4">12. Contato</h2>
          <p>
            Se você tiver dúvidas ou preocupações sobre esta Política de Privacidade ou sobre nossas práticas de privacidade, entre em contato conosco pelo email: <a href="mailto:privacidade@musiclearning.com">privacidade@musiclearning.com</a>
          </p>
        </div>

        <!-- Print Button -->
        <div class="mt-8 text-center">
          <button 
            @click="printPolicy" 
            class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 mx-auto"
          >
            <Printer class="h-5 w-5" />
            Imprimir Política
          </button>
        </div>
      </div>

      <!-- Cookie Preferences -->
      <div class="mt-8 bg-blue-50 rounded-lg p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Preferências de Cookies</h3>
        <p class="text-gray-700 mb-4">
          Você pode gerenciar suas preferências de cookies a qualquer momento. Suas escolhas serão salvas para este navegador e dispositivo.
        </p>
        
        <div class="space-y-4 mt-6">
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-medium text-gray-900">Cookies Essenciais</h4>
              <p class="text-sm text-gray-600">Necessários para o funcionamento básico do site</p>
            </div>
            <div class="relative">
              <input type="checkbox" checked disabled class="sr-only peer" />
              <div class="w-11 h-6 bg-gray-300 rounded-full peer peer-checked:bg-blue-600"></div>
              <div class="absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition peer-checked:translate-x-5"></div>
            </div>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-medium text-gray-900">Cookies de Desempenho</h4>
              <p class="text-sm text-gray-600">Ajudam a melhorar a performance e experiência do site</p>
            </div>
            <div class="relative">
              <input type="checkbox" id="performance" v-model="cookiePreferences.performance" class="sr-only peer" />
              <label for="performance" class="w-11 h-6 bg-gray-300 rounded-full peer-checked:bg-blue-600 block cursor-pointer"></label>
              <div class="absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition peer-checked:translate-x-5"></div>
            </div>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-medium text-gray-900">Cookies de Marketing</h4>
              <p class="text-sm text-gray-600">Usados para publicidade personalizada</p>
            </div>
            <div class="relative">
              <input type="checkbox" id="marketing" v-model="cookiePreferences.marketing" class="sr-only peer" />
              <label for="marketing" class="w-11 h-6 bg-gray-300 rounded-full peer-checked:bg-blue-600 block cursor-pointer"></label>
              <div class="absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition peer-checked:translate-x-5"></div>
            </div>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h4 class="font-medium text-gray-900">Cookies de Análise</h4>
              <p class="text-sm text-gray-600">Ajudam a entender como os visitantes interagem com o site</p>
            </div>
            <div class="relative">
              <input type="checkbox" id="analytics" v-model="cookiePreferences.analytics" class="sr-only peer" />
              <label for="analytics" class="w-11 h-6 bg-gray-300 rounded-full peer-checked:bg-blue-600 block cursor-pointer"></label>
              <div class="absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition peer-checked:translate-x-5"></div>
            </div>
          </div>
        </div>
        
        <div class="mt-6 flex justify-center">
          <button 
            @click="saveCookiePreferences" 
            class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Salvar Preferências
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Printer, ChevronRight } from 'lucide-vue-next'

const cookiePreferences = ref({
  performance: true,
  marketing: false,
  analytics: true
})

const sections = [
  {
    title: 'Informações que Coletamos',
    content: `
      <p>Podemos coletar os seguintes tipos de informações:</p>
      <ul>
        <li><strong>Informações de Cadastro:</strong> Nome, endereço de email, senha, data de nascimento e outras informações fornecidas durante o registro.</li>
        <li><strong>Informações de Perfil:</strong> Foto, biografia, interesses musicais e outras informações que você opta por compartilhar.</li>
        <li><strong>Informações de Uso:</strong> Dados sobre como você interage com nossa plataforma, incluindo cursos acessados, tempo gasto, progresso de aprendizado e preferências.</li>
        <li><strong>Informações de Dispositivo:</strong> Tipo de dispositivo, sistema operacional, navegador, endereço IP e identificadores de dispositivo.</li>
        <li><strong>Informações de Pagamento:</strong> Dados de cartão de crédito, informações de faturamento e histórico de transações.</li>
      </ul>
    `
  },
  {
    title: 'Como Usamos Suas Informações',
    content: `
      <p>Utilizamos suas informações para os seguintes fins:</p>
      <ul>
        <li>Fornecer, manter e melhorar nossos serviços</li>
        <li>Processar transações e gerenciar sua conta</li>
        <li>Personalizar sua experiência de aprendizado</li>
        <li>Enviar comunicações relacionadas ao serviço</li>
        <li>Enviar materiais promocionais e newsletters (se você optar por recebê-los)</li>
        <li>Analisar tendências de uso e melhorar nossa plataforma</li>
        <li>Detectar, prevenir e resolver problemas técnicos e de segurança</li>
        <li>Cumprir obrigações legais</li>
      </ul>
    `
  },
  {
    title: 'Compartilhamento de Informações',
    content: `
      <p>Podemos compartilhar suas informações nas seguintes circunstâncias:</p>
      <ul>
        <li><strong>Com Prestadores de Serviços:</strong> Empresas que nos ajudam a fornecer e melhorar nossos serviços (processamento de pagamentos, hospedagem, análise de dados).</li>
        <li><strong>Com Instrutores:</strong> Informações limitadas sobre seu progresso e participação em cursos específicos.</li>
        <li><strong>Para Conformidade Legal:</strong> Quando necessário para cumprir obrigações legais, proteger nossos direitos ou responder a solicitações governamentais.</li>
        <li><strong>Com Seu Consentimento:</strong> Em outras circunstâncias, com seu consentimento explícito.</li>
      </ul>
      <p>Não vendemos suas informações pessoais a terceiros.</p>
    `
  },
  {
    title: 'Cookies e Tecnologias Semelhantes',
    content: `
      <p>Utilizamos cookies e tecnologias semelhantes para:</p>
      <ul>
        <li>Manter você conectado à sua conta</li>
        <li>Lembrar suas preferências</li>
        <li>Entender como você usa nossa plataforma</li>
        <li>Melhorar nossos serviços</li>
        <li>Personalizar conteúdo e publicidade</li>
      </ul>
      <p>Você pode gerenciar suas preferências de cookies através das configurações do seu navegador ou através das opções disponíveis em nossa plataforma.</p>
    `
  },
  {
    title: 'Segurança de Dados',
    content: `
      <p>Implementamos medidas de segurança técnicas e organizacionais para proteger suas informações pessoais, incluindo:</p>
      <ul>
        <li>Criptografia de dados sensíveis</li>
        <li>Acesso restrito a informações pessoais</li>
        <li>Monitoramento de segurança contínuo</li>
        <li>Avaliações regulares de segurança</li>
      </ul>
      <p>No entanto, nenhum método de transmissão pela Internet ou método de armazenamento eletrônico é 100% seguro, e não podemos garantir segurança absoluta.</p>
    `
  },
  {
    title: 'Retenção de Dados',
    content: `
      <p>Mantemos suas informações pessoais pelo tempo necessário para fornecer nossos serviços e cumprir nossas obrigações legais. Quando suas informações não forem mais necessárias, as excluiremos ou anonimizaremos.</p>
    `
  },
  {
    title: 'Seus Direitos',
    content: `
      <p>Dependendo da sua localização, você pode ter os seguintes direitos em relação às suas informações pessoais:</p>
      <ul>
        <li>Acessar e receber uma cópia de suas informações pessoais</li>
        <li>Corrigir informações imprecisas ou incompletas</li>
        <li>Excluir suas informações pessoais</li>
        <li>Restringir ou opor-se ao processamento de suas informações</li>
        <li>Portabilidade de dados</li>
        <li>Retirar consentimento</li>
      </ul>
      <p>Para exercer esses direitos, entre em contato conosco através dos canais indicados abaixo.</p>
    `
  },
  {
    title: 'Transferências Internacionais de Dados',
    content: `
      <p>Suas informações podem ser transferidas e processadas em países diferentes do seu país de residência. Implementamos salvaguardas apropriadas para proteger suas informações durante essas transferências.</p>
    `
  },
  {
    title: 'Privacidade de Crianças',
    content: `
      <p>Nossos serviços não são direcionados a pessoas menores de 13 anos. Não coletamos intencionalmente informações pessoais de crianças menores de 13 anos. Se tomarmos conhecimento de que coletamos informações pessoais de uma criança menor de 13 anos, tomaremos medidas para excluir essas informações.</p>
    `
  },
  {
    title: 'Alterações nesta Política',
    content: `
      <p>Podemos atualizar esta Política de Privacidade periodicamente. Notificaremos você sobre alterações significativas publicando a nova política em nossa plataforma e, quando apropriado, enviando uma notificação por email.</p>
    `
  },
  {
    title: 'Seus Direitos de Privacidade na Califórnia',
    content: `
      <p>Se você é residente da Califórnia, você tem direitos específicos sob a Lei de Privacidade do Consumidor da Califórnia (CCPA). Para mais informações sobre esses direitos e como exercê-los, consulte nossa <a href="#" class="text-blue-600 hover:text-blue-800 hover:underline">Notificação de Privacidade da Califórnia</a>.</p>
    `
  }
]

const printPolicy = () => {
  window.print()
}

const saveCookiePreferences = () => {
  console.log('Cookie preferences saved:', cookiePreferences.value)
  alert('Suas preferências de cookies foram salvas com sucesso!')
}
</script>

<style scoped>
.prose h2 {
  @apply text-xl font-semibold text-gray-900 mt-8 mb-4;
}

.prose p {
  @apply text-gray-700 leading-relaxed mb-4;
}

.prose ul {
  @apply list-disc list-inside space-y-1 mb-6 text-gray-700 ml-4;
}

.prose a {
  @apply text-blue-600 hover:text-blue-800 underline;
}

@media print {
  button, .cookie-preferences {
    display: none !important;
  }
}
</style>