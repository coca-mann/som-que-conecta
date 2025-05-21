// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // Nossa configuração de rotas
import './assets/tailwind.css' // Certifique-se que o caminho está correto

const app = createApp(App)

app.use(router) // Diz ao Vue para usar o router

app.mount('#app')