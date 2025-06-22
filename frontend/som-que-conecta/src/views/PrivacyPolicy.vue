<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="text-center mb-10">
        <h1 class="text-3xl font-bold text-gray-900 mb-3">
          Política de Privacidade
        </h1>
        <p class="text-gray-600">
          Última atualização: 22 de junho de 2025
        </p>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-8">
        <div class="prose max-w-none">
          <p class="text-gray-700 mb-6">
            Bem-vindo ao <strong>Som que Conecta</strong>. A sua privacidade é uma de nossas maiores prioridades. Esta Política de Privacidade explica como coletamos, usamos e protegemos suas informações quando você utiliza nossa plataforma gratuita de educação musical.
          </p>

          <div v-for="(section, index) in sections" :key="index" class="mb-8">
            <h2 :id="`section-${index + 1}`" class="text-xl font-semibold text-gray-900 mb-4">
              {{ index + 1 }}. {{ section.title }}
            </h2>
            <div v-html="section.content" class="space-y-4" />
          </div>

          <h2 id="contact" class="text-xl font-semibold text-gray-900 mb-4">
            {{ sections.length + 1 }}. Contato
          </h2>
          <p>
            Se você tiver dúvidas sobre esta Política de Privacidade, entre em contato conosco pelo e-mail: <a href="mailto:contato@somqueconecta.fun" class="text-red-600 hover:underline">contato@somqueconecta.fun</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useHead } from '@vueuse/head';

useHead({
  title: 'Política de Privacidade | Som que Conecta',
  meta: [
    { name: 'description', content: 'Entenda como coletamos, usamos e protegemos seus dados na plataforma Som que Conecta.' },
  ]
})

// O conteúdo da política agora é gerenciado aqui
const sections = ref([
  {
    title: 'Informações que Coletamos',
    content: `
      <p>Para fornecer nossos serviços, coletamos as seguintes informações:</p>
      <ul>
        <li><strong>Informações de Cadastro:</strong> Seu nome, sobrenome, endereço de e-mail e senha (criptografada).</li>
        <li><strong>Informações de Perfil:</strong> Dados que você opta por adicionar, como foto de perfil, biografia, nível de habilidade musical e se você atua como Professor ou ONG.</li>
        <li><strong>Conteúdo Gerado pelo Usuário:</strong> Artigos, comentários e avaliações que você cria e publica na plataforma.</li>
        <li><strong>Informações de Progresso:</strong> Registros das tarefas e minicursos que você conclui para que possamos calcular seu progresso e nível de habilidade.</li>
        <li><strong>Informações de Uso:</strong> Dados anônimos sobre como você interage com o site (quais páginas visita, etc.) para nos ajudar a melhorar a plataforma.</li>
      </ul>
    `
  },
  {
    title: 'Como Usamos Suas Informações',
    content: `
      <p>Utilizamos suas informações estritamente para:</p>
      <ul>
        <li>Fornecer e manter os serviços da plataforma, como exibir seu progresso nos cursos.</li>
        <li>Personalizar sua experiência de aprendizado.</li>
        <li>Permitir a comunicação entre usuários e provedores de instrumentos no processo de agendamento.</li>
        <li>Exibir seu conteúdo público, como artigos e comentários, atribuindo a autoria a você.</li>
        <li>Enviar comunicações importantes sobre sua conta ou sobre os serviços (ex: e-mail de redefinição de senha).</li>
        <li>Garantir a segurança da plataforma e prevenir fraudes.</li>
      </ul>
    `
  },
  {
    title: 'Compartilhamento de Informações',
    content: `
      <p>Sua privacidade é fundamental. Nós não vendemos suas informações pessoais. O compartilhamento de dados ocorre apenas nas seguintes situações:</p>
      <ul>
        <li><strong>Informações Públicas:</strong> Seu nome de usuário e foto de perfil são visíveis publicamente em conteúdos que você cria, como artigos e comentários.</li>
        <li><strong>Empréstimo de Instrumentos:</strong> Ao solicitar um instrumento, suas informações de contato (como e-mail) podem ser compartilhadas com o Professor ou ONG responsável para que eles possam coordenar o empréstimo com você.</li>
        <li><strong>Obrigações Legais:</strong> Se formos obrigados por lei ou por uma ordem judicial a compartilhar informações.</li>
      </ul>
    `
  },
  {
    title: 'Cookies e Tecnologias Essenciais',
    content: `
      <p>Utilizamos tecnologias como cookies e armazenamento local (localStorage) estritamente para o funcionamento essencial da plataforma. Isso inclui:</p>
      <ul>
        <li><strong>Cookies de Autenticação:</strong> Para manter sua sessão ativa e segura enquanto você navega pelo site.</li>
        <li><strong>Armazenamento de Preferências:</strong> Para lembrar de suas configurações, como o modo de visualização de uma lista.</li>
      </ul>
      <p>No momento, não utilizamos cookies para fins de marketing ou publicidade de terceiros. Caso isso mude no futuro, esta política será atualizada e você será notificado para gerenciar suas preferências.</p>
    `
  },
  {
    title: 'Seus Direitos e Controle',
    content: `
      <p>De acordo com a Lei Geral de Proteção de Dados (LGPD) do Brasil, você tem o direito de acessar, corrigir, atualizar e solicitar a exclusão de suas informações pessoais. Você pode gerenciar a maioria dos seus dados diretamente na página do seu perfil ou entrando em contato conosco.</p>
    `
  },
  {
    title: 'Segurança e Retenção de Dados',
    content: `
      <p>Implementamos medidas de segurança para proteger suas informações. Seus dados são mantidos em nossa plataforma apenas enquanto sua conta estiver ativa ou pelo tempo necessário para cumprirmos nossas obrigações legais.</p>
    `
  }
])
</script>

<style scoped>
.prose h2 {
  @apply text-xl font-semibold text-gray-900 mt-8 mb-4;
}
.prose p, .prose ul {
  @apply text-gray-700 leading-relaxed mb-4;
}
.prose ul {
  @apply list-disc list-inside space-y-2 mb-6 ml-4;
}
.prose li::marker {
  color: #DC2626; /* Cor vermelha para os marcadores da lista */
}
.prose a {
  @apply text-red-600 hover:text-red-800 underline;
}
</style>