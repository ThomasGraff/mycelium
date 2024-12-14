<template>
  <v-app class="app-container">
    <v-app-bar v-if="isAuthenticated" app color="primary" dark>
      <v-toolbar-title>Mycelium</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text @click="logout">Logout</v-btn>
    </v-app-bar>

    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import { defineComponent, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import auth from '@/services/auth'

export default defineComponent({
  name: 'App',
  setup() {
    const router = useRouter()
    const isAuthenticated = ref(false)

    onMounted(async () => {
      try {
        //await auth.getCurrentUser()
        //isAuthenticated.value = auth.isAuthenticated
      } catch (error) {
        console.error('❌ Failed to get user:', error)
      }
    })

    const logout = async () => {
      await auth.logout()
      router.push('/login')
    }

    return {
      isAuthenticated,
      logout
    }
  }
})
</script>

<style>
:root {
  --scrollbar-color: #212121;
}

html, body {
  height: 100%;
  overflow: hidden;
}

.app-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Global scrollbar styles */
* {
  scrollbar-width: thin;
  scrollbar-color: var(--scrollbar-color) transparent;
}

/* WebKit browsers (Chrome, Safari, etc.) */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background-color: var(--scrollbar-color);
  border-radius: 10px;
  border: 2px solid transparent;
  background-clip: padding-box;
}

::-webkit-scrollbar-button {
  display: none;
}
</style>
