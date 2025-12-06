import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import '@fontsource/inter/400.css'
import '@fontsource/inter/500.css'
import '@fontsource/inter/600.css'
import '@fontsource/inter/700.css'
import '@fontsource/jetbrains-mono/400.css'
import './assets/main.css'

const app = createApp(App)

// Configuration Pinia
app.use(createPinia())

// Configuration du routeur
app.use(router)

app.mount('#app')
