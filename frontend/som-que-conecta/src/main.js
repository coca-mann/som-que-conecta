import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createHead } from '@vueuse/head'
import Vue3GoogleLogin from 'vue3-google-login'

import App from './App.vue'
import router from './router'

import './assets/tailwind.css'
import './assets/style.css'

const app = createApp(App)
const head = createHead()

app.use(createPinia())
app.use(router)
app.use(head)
app.use(Vue3GoogleLogin, {
    clientId: 'SEU_CLIENT_ID_AQUI'
  })

app.mount('#app')