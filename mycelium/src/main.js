import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import router from './router'
import auth from './services/auth'

loadFonts()

const app = createApp(App)
app.use(vuetify)
app.use(router)

// Initialize auth service before mounting the app
auth.initialize().then(() => {
  app.mount('#app')
})



