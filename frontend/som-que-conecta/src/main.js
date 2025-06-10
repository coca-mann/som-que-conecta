// src/main.js - A ORDEM CORRETA E DEFINITIVA

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import './assets/tailwind.css'

// 1. Crie a instância da aplicação
const app = createApp(App)

// 2. PRIMEIRO, INSTALE O PINIA.
// Isso garante que qualquer componente importado a seguir,
// incluindo o App e seus filhos, já encontre um Pinia ativo.
app.use(createPinia()) 

// 3. DEPOIS, INSTALE O ROUTER.
app.use(router)

// 4. FINALMENTE, MONTE A APLICAÇÃO.
app.mount('#app')