<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <!-- Header -->
      <div class="text-center mb-10">
        <h1 class="text-3xl font-bold text-gray-900 mb-3">Termos de Uso</h1>
        <p class="text-gray-600">
          Última atualização: 5 de junho de 2024
        </p>
      </div>

      <!-- Terms Content -->
      <div class="bg-white rounded-lg shadow-sm p-8">
        <div class="prose max-w-none">
          <h2>1. Aceitação dos Termos</h2>
          <p>
            Ao acessar e usar a plataforma Music Learning, você concorda em cumprir e estar vinculado aos seguintes termos e condições de uso. Se você não concordar com qualquer parte destes termos, não poderá acessar ou utilizar nossos serviços.
          </p>

          <h2>2. Descrição do Serviço</h2>
          <p>
            A Music Learning é uma plataforma educacional online dedicada ao ensino de música, oferecendo cursos, artigos, tutoriais e ferramentas para aprendizado musical. Nossos serviços incluem, mas não se limitam a:
          </p>
          <ul>
            <li>Cursos de música online</li>
            <li>Artigos e conteúdo educacional</li>
            <li>Ferramentas de prática e aprendizado</li>
            <li>Comunidade de estudantes e professores</li>
            <li>Recursos para gerenciamento de instrumentos</li>
          </ul>

          <h2>3. Cadastro e Conta</h2>
          <p>
            Para acessar determinados recursos da plataforma, você precisará criar uma conta. Ao se cadastrar, você concorda em:
          </p>
          <ul>
            <li>Fornecer informações verdadeiras, precisas e completas</li>
            <li>Manter e atualizar prontamente seus dados cadastrais</li>
            <li>Manter a segurança de sua senha e identificação</li>
            <li>Ser integralmente responsável por todas as atividades realizadas com sua conta</li>
            <li>Notificar imediatamente qualquer uso não autorizado de sua conta</li>
          </ul>

          <h2>4. Conteúdo e Propriedade Intelectual</h2>
          <p>
            Todo o conteúdo disponibilizado na plataforma Music Learning, incluindo textos, gráficos, logotipos, ícones, imagens, clipes de áudio, downloads digitais, compilações de dados e software, é propriedade da Music Learning ou de seus fornecedores de conteúdo e está protegido pelas leis de direitos autorais.
          </p>
          <p>
            Você não pode modificar, reproduzir, distribuir, transmitir, exibir, publicar, vender, licenciar, criar trabalhos derivados ou usar qualquer conteúdo disponível na plataforma para fins comerciais sem o consentimento prévio por escrito da Music Learning.
          </p>

          <h2>5. Conduta do Usuário</h2>
          <p>
            Ao utilizar nossa plataforma, você concorda em não:
          </p>
          <ul>
            <li>Violar quaisquer leis ou regulamentos aplicáveis</li>
            <li>Publicar ou transmitir material ilegal, ameaçador, difamatório, obsceno ou ofensivo</li>
            <li>Interferir ou interromper o funcionamento da plataforma</li>
            <li>Tentar acessar áreas restritas da plataforma</li>
            <li>Usar a plataforma para fins comerciais não autorizados</li>
            <li>Coletar informações de outros usuários sem consentimento</li>
            <li>Fazer upload de vírus ou outros códigos maliciosos</li>
          </ul>

          <h2>6. Assinaturas e Pagamentos</h2>
          <p>
            Alguns serviços da Music Learning podem exigir pagamento ou assinatura. Ao adquirir uma assinatura, você concorda com os seguintes termos:
          </p>
          <ul>
            <li>Fornecer informações de pagamento precisas e completas</li>
            <li>Autorizar a cobrança pelos serviços selecionados</li>
            <li>Manter suas informações de pagamento atualizadas</li>
            <li>Entender que as assinaturas são renovadas automaticamente até que sejam canceladas</li>
            <li>Aceitar nossa política de reembolso conforme descrita nos termos específicos de cada serviço</li>
          </ul>

          <h2>7. Cancelamento e Rescisão</h2>
          <p>
            Você pode cancelar sua conta a qualquer momento. A Music Learning reserva-se o direito de suspender ou encerrar sua conta e acesso à plataforma se você violar estes Termos de Uso ou por qualquer outro motivo a nosso critério exclusivo.
          </p>

          <h2>8. Limitação de Responsabilidade</h2>
          <p>
            A Music Learning não será responsável por quaisquer danos diretos, indiretos, incidentais, especiais, consequenciais ou punitivos resultantes do uso ou incapacidade de usar nossos serviços, incluindo, mas não se limitando a, perda de lucros, dados, uso, boa vontade ou outras perdas intangíveis.
          </p>

          <h2>9. Modificações dos Termos</h2>
          <p>
            A Music Learning reserva-se o direito de modificar estes Termos de Uso a qualquer momento. As alterações entrarão em vigor imediatamente após a publicação dos termos atualizados. O uso contínuo da plataforma após tais alterações constitui sua aceitação dos novos termos.
          </p>

          <h2>10. Lei Aplicável</h2>
          <p>
            Estes Termos de Uso serão regidos e interpretados de acordo com as leis do Brasil, independentemente de conflitos de disposições legais.
          </p>

          <h2>11. Contato</h2>
          <p>
            Se você tiver dúvidas sobre estes Termos de Uso, entre em contato conosco pelo email: <a href="mailto:termos@musiclearning.com">termos@musiclearning.com</a>
          </p>
        </div>

        <!-- Print Button -->
        <div class="mt-8 text-center">
          <button 
            @click="printTerms" 
            class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2 mx-auto"
          >
            <Printer class="h-5 w-5" />
            Imprimir Termos
          </button>
        </div>
      </div>

      <!-- Acceptance Section -->
      <div class="mt-8 bg-blue-50 rounded-lg p-6 text-center">
        <p class="text-gray-700 mb-4">
          Ao utilizar nossa plataforma, você confirma que leu, entendeu e concorda com estes Termos de Uso.
        </p>
        <router-link 
          to="/" 
          class="inline-flex items-center px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Voltar para a Página Inicial
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Printer } from 'lucide-vue-next'

const printTerms = () => {
  window.print()
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
  button {
    display: none !important;
  }
}
</style>