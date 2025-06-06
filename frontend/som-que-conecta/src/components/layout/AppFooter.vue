<template>
  <footer class="bg-gray-900 text-white mt-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid md:grid-cols-4 gap-8">
        <div>
          <div class="flex items-center space-x-2 mb-4">
            <Music class="h-8 w-8 text-blue-400" />
            <span class="text-xl font-bold">MusicLearn</span>
          </div>
          <p class="text-gray-400 mb-4">
            Sua plataforma completa para aprender música do zero. 
            Conectamos estudantes, professores e instrumentos.
          </p>
          <div class="flex space-x-4">
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              <Facebook class="h-5 w-5" />
            </a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              <Instagram class="h-5 w-5" />
            </a>
            <a href="#" class="text-gray-400 hover:text-white transition-colors">
              <Youtube class="h-5 w-5" />
            </a>
          </div>
        </div>
        
        <div>
          <h3 class="text-lg font-semibold mb-4">Navegação</h3>
          <ul class="space-y-2">
            <li><a @click="handleNavigation('/')" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Início</a></li>
            <li><a @click="handleNavigation('/articles')" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Artigos</a></li>
            <li><a @click="handleNavigation('/instruments')" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Instrumentos</a></li>
            <li><a @click="handleNavigation('/courses')" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Minicursos</a></li>
          </ul>
        </div>
        
        <div>
          <h3 class="text-lg font-semibold mb-4">Suporte</h3>
          <ul class="space-y-2">
            <li><a @click="handleNavigation('/help')" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Central de Ajuda</a></li>
            <li><a @click="handleNavigation('/contact')" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Contato</a></li>
            <li><a @click="handleNavigation('/terms')" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Termos de Uso</a></li>
            <li><a @click="handleNavigation('/privacy')" class="text-gray-400 hover:text-white transition-colors cursor-pointer">Política de Privacidade</a></li>
          </ul>
        </div>
        
        <div>
          <h3 class="text-lg font-semibold mb-4">Newsletter</h3>
          <p class="text-gray-400 mb-4">
            Receba dicas musicais e novidades em seu email
          </p>
          <form class="space-y-2">
            <input 
              type="email" 
              placeholder="Seu email" 
              class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white placeholder-gray-400"
            >
            <button 
              type="submit" 
              class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Inscrever-se
            </button>
          </form>
        </div>
      </div>
      
      <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
        <p>&copy; 2024 MusicLearn. Todos os direitos reservados.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { Music, Facebook, Instagram, Youtube } from 'lucide-vue-next'
import { useRouter } from 'vue-router'

const router = useRouter()

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

const handleNavigation = (to) => {
  router.push(to)
  scrollToTop()
}
</script> 