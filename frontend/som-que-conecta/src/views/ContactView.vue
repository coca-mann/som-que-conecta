<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto px-0 sm:px-6 lg:px-8 py-12">
      <div class="text-center mb-12">
        <h1 class="text-3xl font-bold text-gray-900 mb-3">
          Entre em Contato
        </h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto">
          Estamos sempre disponíveis para ajudar e ouvir suas sugestões. Escolha o canal que preferir.
        </p>
      </div>

      <div class="grid md:grid-cols-2 gap-8 mb-12">
        <div class="bg-white rounded-lg shadow-sm p-8 text-center">
          <div class="inline-flex items-center justify-center h-16 w-16 rounded-full bg-red-100 mb-6">
            <Mail class="h-8 w-8 text-red-600" />
          </div>
          <h2 class="text-xl font-semibold text-gray-900 mb-3">
            Email
          </h2>
          <p class="text-gray-600 mb-6">
            Para dúvidas, sugestões ou parcerias, envie-nos um email.
          </p>
          <a 
            href="mailto:contato@somqueconecta.fun" 
            class="inline-flex items-center px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
          >
            contato@somqueconecta.fun
          </a>
        </div>

        <div class="bg-white rounded-lg shadow-sm p-8 text-center">
          <div class="inline-flex items-center justify-center h-16 w-16 rounded-full bg-gray-200 mb-6">
            <HelpCircle class="h-8 w-8 text-gray-700" />
          </div>
          <h2 class="text-xl font-semibold text-gray-900 mb-3">
            Suporte
          </h2>
          <p class="text-gray-600 mb-6">
            Precisa de ajuda? Nossa equipe de suporte está pronta para atendê-lo.
          </p>
          <a 
            href="mailto:contato@somqueconecta.fun" 
            class="inline-flex items-center px-6 py-3 bg-gray-700 text-white rounded-lg hover:bg-gray-800 transition-colors"
          >
            contato@somqueconecta.fun
          </a>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-8 mb-12">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 text-center">
          Redes Sociais
        </h2>
        
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <a 
            href="#" 
            target="_blank" 
            rel="noopener noreferrer"
            class="flex flex-col items-center p-6 rounded-lg hover:bg-gray-50 transition-colors group"
          >
            <div class="inline-flex items-center justify-center h-14 w-14 rounded-full bg-gradient-to-tr from-purple-600 to-pink-500 mb-4 group-hover:scale-110 transition-transform">
              <Instagram class="h-7 w-7 text-white" />
            </div>
            <h3 class="font-medium text-gray-900">Instagram</h3>
            <p class="text-sm text-gray-500">@somqueconecta</p>
          </a>

          <a 
            href="#" 
            target="_blank" 
            rel="noopener noreferrer"
            class="flex flex-col items-center p-6 rounded-lg hover:bg-gray-50 transition-colors group"
          >
            <div class="inline-flex items-center justify-center h-14 w-14 rounded-full bg-blue-600 mb-4 group-hover:scale-110 transition-transform">
              <Facebook class="h-7 w-7 text-white" />
            </div>
            <h3 class="font-medium text-gray-900">Facebook</h3>
            <p class="text-sm text-gray-500">/somqueconecta</p>
          </a>

          <a 
            href="#" 
            target="_blank" 
            rel="noopener noreferrer"
            class="flex flex-col items-center p-6 rounded-lg hover:bg-gray-50 transition-colors group"
          >
            <div class="inline-flex items-center justify-center h-14 w-14 rounded-full bg-red-600 mb-4 group-hover:scale-110 transition-transform">
              <Youtube class="h-7 w-7 text-white" />
            </div>
            <h3 class="font-medium text-gray-900">YouTube</h3>
            <p class="text-sm text-gray-500">/somqueconecta</p>
          </a>

          <a 
            href="#" 
            target="_blank" 
            rel="noopener noreferrer"
            class="flex flex-col items-center p-6 rounded-lg hover:bg-gray-50 transition-colors group"
          >
            <div class="inline-flex items-center justify-center h-14 w-14 rounded-full bg-blue-400 mb-4 group-hover:scale-110 transition-transform">
              <Twitter class="h-7 w-7 text-white" />
            </div>
            <h3 class="font-medium text-gray-900">Twitter</h3>
            <p class="text-sm text-gray-500">@somqueconecta</p>
          </a>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-8 mb-12">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 text-center">
          Horário de Atendimento
        </h2>
        
        <div class="max-w-md mx-auto">
          <div class="space-y-3">
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="font-medium text-gray-900">Segunda a Sexta</span>
              <span class="text-gray-600">9:00 - 18:00</span>
            </div>
            <div class="flex justify-between py-2 border-b border-gray-100">
              <span class="font-medium text-gray-900">Sábado</span>
              <span class="text-gray-600">10:00 - 15:00</span>
            </div>
            <div class="flex justify-between py-2">
              <span class="font-medium text-gray-900">Domingo e Feriados</span>
              <span class="text-gray-600">Fechado</span>
            </div>
          </div>
          
          <div class="mt-6 text-center text-gray-600">
            <p>Responderemos todas as mensagens dentro do nosso horário de atendimento.</p>
            <p class="mt-2">
              Tempo médio de resposta: 24 horas úteis.
            </p>
          </div>
        </div>
      </div>

      <div class="bg-red-50 rounded-lg shadow-sm p-8">
        <div class="max-w-2xl mx-auto text-center">
          <h2 class="text-2xl font-bold text-gray-900 mb-3">
            Fique por dentro das novidades
          </h2>
          <p class="text-gray-600 mb-6">
            Assine nossa newsletter e receba dicas, novidades e conteúdos exclusivos sobre música.
          </p>
          
          <form
            class="flex flex-col sm:flex-row gap-3"
            @submit.prevent="subscribeNewsletter"
          >
            <input 
              v-model="newsletterEmail"
              type="email" 
              required
              placeholder="Seu melhor email"
              class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent"
            >
            <button 
              type="submit"
              class="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors whitespace-nowrap"
            >
              Assinar Newsletter
            </button>
          </form>
          
          <p class="text-xs text-gray-500 mt-4">
            Ao assinar, você concorda com nossa Política de Privacidade. Você pode cancelar a qualquer momento.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { 
  Mail, 
  HelpCircle, 
  Instagram, 
  Facebook, 
  Youtube, 
  Twitter 
} from 'lucide-vue-next'
import { useHead } from '@vueuse/head';

useHead({
  title: 'Contato | Som que Conecta',
  meta: [
    { name: 'description', content: 'Informações de contato com a equipe Som que Conecta.' },
  ]
})

const newsletterEmail = ref('')

const subscribeNewsletter = () => {
  console.log('Newsletter subscription:', newsletterEmail.value)
  alert(`Obrigado por assinar nossa newsletter! Um email de confirmação foi enviado para ${newsletterEmail.value}`)
  newsletterEmail.value = ''
}
</script>