<template>
  <footer class="bg-gray-900 text-white mt-auto relative z-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid md:grid-cols-3 gap-8">
        <div>
          <div class="flex items-center space-x-2 mb-4">
            <img 
              :src="logoImage" 
              alt="Som que Conecta Logo"
              class="h-14 w-14 object-contain"
            >
            <span class="text-xl font-bold">Som que Conecta</span>
          </div>
          <p class="text-gray-400 mb-4">
            Sua plataforma completa para aprender música do zero. 
            Conectamos estudantes, professores e instrumentos.
          </p>
        </div>
        
        <div>
          <h3 class="text-lg font-semibold mb-4">
            Navegação
          </h3>
          <ul class="space-y-2">
            <li>
              <a
                class="text-gray-400 hover:text-red-500 transition-colors cursor-pointer"
                @click="handleNavigation('/')"
              >Início</a>
            </li>
            <li>
              <a
                class="text-gray-400 hover:text-red-500 transition-colors cursor-pointer"
                @click="handleNavigation('/articles')"
              >Artigos</a>
            </li>
            <li>
              <a
                class="text-gray-400 hover:text-red-500 transition-colors cursor-pointer"
                @click="handleNavigation('/instruments')"
              >Instrumentos</a>
            </li>
            <li>
              <a
                class="text-gray-400 hover:text-red-500 transition-colors cursor-pointer"
                @click="handleNavigation('/courses')"
              >Minicursos</a>
            </li>
          </ul>
        </div>
        
        <div>
          <h3 class="text-lg font-semibold mb-4">
            Suporte
          </h3>
          <ul class="space-y-2">
            <li>
              <a
                class="text-gray-400 hover:text-red-500 transition-colors cursor-pointer"
                @click="handleNavigation('/help')"
              >Central de Ajuda</a>
            </li>
            <li>
              <a
                class="text-gray-400 hover:text-red-500 transition-colors cursor-pointer"
                @click="handleNavigation('/terms')"
              >Termos de Uso</a>
            </li>
            <li>
              <a
                class="text-gray-400 hover:text-red-500 transition-colors cursor-pointer"
                @click="handleNavigation('/privacy')"
              >Política de Privacidade</a>
            </li>
          </ul>
        </div>
      </div>
      
      <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
        <p>&copy; 2025 Som que Conecta. Todos os direitos reservados.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { Facebook, Instagram, Youtube } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import logoImage from '@/assets/logo.png'

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