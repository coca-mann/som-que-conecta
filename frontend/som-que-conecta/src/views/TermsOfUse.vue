<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="text-center mb-10">
        <h1 class="text-3xl font-bold text-gray-900 mb-3">
          Termos de Uso
        </h1>
        <p class="text-gray-600">
          Última atualização: 22 de junho de 2025
        </p>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-8">
        <div class="prose max-w-none">
          <h2>1. Bem-vindo ao Som que Conecta!</h2>
          <p>
            Ao acessar ou usar a plataforma "Som que Conecta" ("Plataforma"), você concorda em cumprir e estar vinculado a estes Termos de Uso ("Termos"). Se você não concordar com qualquer parte destes termos, você não deve acessar ou utilizar nossos serviços.
          </p>

          <h2>2. Nossos Serviços</h2>
          <p>
            O Som que Conecta é uma plataforma dedicada a democratizar o acesso à educação musical. Nossos serviços, oferecidos gratuitamente, incluem:
          </p>
          <ul>
            <li><strong>Minicursos Estruturados:</strong> Cursos com tarefas sequenciais que permitem aos usuários aprender e acompanhar seu próprio progresso.</li>
            <li><strong>Artigos Educacionais:</strong> Conteúdo informativo e prático criado por nossa comunidade de professores e especialistas.</li>
            <li><strong>Empréstimo de Instrumentos:</strong> Uma funcionalidade que conecta usuários que desejam aprender com ONGs e professores que disponibilizam instrumentos para empréstimo.</li>
          </ul>

          <h2>3. Cadastro e Contas de Usuário</h2>
          <p>
            Para acessar a maioria dos recursos, você precisará criar uma conta. Ao se cadastrar, você concorda em fornecer informações verdadeiras e completas, e é responsável por manter a segurança de sua senha e por todas as atividades em sua conta. A plataforma pode oferecer diferentes tipos de perfil (ex: Aluno, Professor, ONG), que podem ter diferentes permissões e exigir validação pela nossa equipe.
          </p>

          <h2>4. Propriedade Intelectual</h2>
          <h3>4.1. Conteúdo da Plataforma</h3>
          <p>
            Todo o conteúdo disponibilizado pela Som que Conecta, como a estrutura dos cursos, design e software, é de nossa propriedade e protegido por leis de direitos autorais.
          </p>
          <h3>4.2. Conteúdo Gerado pelo Usuário</h3>
          <p>
            Os usuários com perfil de Professor ou ONG podem criar e publicar conteúdo, como artigos. Ao publicar conteúdo na Plataforma, você afirma que possui os direitos sobre ele. Você retém todos os seus direitos de propriedade sobre seu conteúdo, mas concede à Som que Conecta uma licença mundial, não exclusiva e isenta de royalties para usar, reproduzir, distribuir e exibir esse conteúdo no âmbito dos serviços da Plataforma.
          </p>

          <h2>5. Empréstimo de Instrumentos</h2>
          <p>
            A Som que Conecta atua como uma **intermediária** para facilitar o contato entre usuários que precisam de um instrumento e parceiros (ONGs, Professores) que os disponibilizam.
          </p>
          <ul>
            <li>O acordo de empréstimo, incluindo termos, duração e responsabilidades, é feito diretamente entre o usuário e o parceiro provedor do instrumento.</li>
            <li>A Som que Conecta não é parte deste acordo e não se responsabiliza pela condição, manutenção, perda, dano ou devolução dos instrumentos.</li>
          </ul>

          <h2>6. Gratuidade do Serviço</h2>
          <p>
            O acesso e uso dos recursos educacionais da Som que Conecta são gratuitos. Nossa plataforma é mantida através de doações, parcerias e trabalho voluntário. Não há taxas de assinatura ou custos para acessar os minicursos e artigos.
          </p>
          
          <h2>7. Conduta do Usuário</h2>
          <p>
            Você concorda em não usar a plataforma para publicar conteúdo ofensivo, violar leis, interferir com o funcionamento do site ou usar indevidamente o sistema de agendamento e empréstimo de instrumentos para assediar ou enganar outros usuários.
          </p>

          <h2>8. Limitação de Responsabilidade</h2>
          <p>
            A plataforma é fornecida "como está". A Som que Conecta não será responsável por quaisquer danos diretos ou indiretos resultantes do uso ou da incapacidade de usar nossos serviços, incluindo as interações relacionadas ao empréstimo de instrumentos.
          </p>

          <h2>9. Modificações dos Termos</h2>
          <p>
            Reservamo-nos o direito de modificar estes Termos a qualquer momento. Notificaremos sobre as alterações, e o uso contínuo da plataforma após a atualização constituirá sua aceitação dos novos termos.
          </p>

          <h2>10. Contato</h2>
          <p>
            Se você tiver dúvidas sobre estes Termos de Uso, entre em contato conosco pelo e-mail: <a href="mailto:contato@somqueconecta.fun" class="text-red-600 hover:underline">contato@somqueconecta.fun</a>
          </p>
        </div>
      </div>
      
      <div class="mt-8 bg-red-50 rounded-lg p-6 text-center">
        <p class="text-gray-700 mb-4">
          Ao utilizar nossa plataforma, você confirma que leu, entendeu e concorda com estes Termos de Uso.
        </p>
        <router-link 
          to="/" 
          class="inline-flex items-center px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          Voltar para a Página Inicial
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useHead } from '@vueuse/head';

useHead({
  title: 'Termos de Uso | Som que Conecta',
  meta: [
    { name: 'description', content: 'Termos de Uso da plataforma Som que Conecta.' },
  ]
})

</script>

<style scoped>
/* O seu CSS scoped continua o mesmo */
.prose h2 {
  @apply text-xl font-semibold text-gray-900 mt-8 mb-4;
}
.prose p, .prose ul {
  @apply text-gray-700 leading-relaxed mb-4;
}
.prose ul {
  @apply list-disc list-inside space-y-1 mb-6 ml-4;
}
.prose a {
  @apply text-blue-600 hover:text-blue-800 underline;
}
@media print {
  body * {
    visibility: hidden;
  }
  .prose, .prose * {
    visibility: visible;
  }
  .prose {
    position: absolute;
    left: 0;
    top: 0;
  }
}
</style>