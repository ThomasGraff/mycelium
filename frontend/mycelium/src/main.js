import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import router from './router'
import mainOidc from './services/auth'

loadFonts()

mainOidc.startup().then(ok => {
  if (ok) {
    const app = createApp(App)
    
    // Install Vuetify before other plugins
    app.use(vuetify)
    mainOidc.useRouter(router)
    app.use(router)
    
    app.mount('#app')
  } else {
    console.error('❌ OIDC startup error')
  }
}).catch(error => {
  console.error('❌ Application startup failed:', error)
})



