// src/main.js
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import router from './router'
import './assets/tailwind.css' // Certifique-se que este caminho está correto

const app = createApp(App)
app.use(router)
app.mount('#app')