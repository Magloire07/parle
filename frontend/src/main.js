import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import './assets/main.css'

const app = createApp(App)

// Configuration Pinia
app.use(createPinia())

// Configuration du routeur
app.use(router)

app.mount('#app')
