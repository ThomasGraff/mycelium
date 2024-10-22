<template>
  <div class="login-container">
    <v-main class="main-content">
      <v-container fluid class="fill-height">
        <v-row align="center" justify="center">
          <v-col cols="12" sm="8" md="6" lg="4">
            <div class="text-center mb-8">
              <img :src="logoSrc" alt="Mycelium Logo" height="120" />
            </div>
            <v-card class="elevation-12" color="#2f2f2f">
              <v-toolbar color="#212121" dark flat>
                <v-toolbar-title>Login</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-btn color="primary" @click="login" block>Login with Authentik</v-btn>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import auth from '@/services/auth'

export default defineComponent({
  name: 'UserLogin',
  setup() {
    const logoSrc = require('@/assets/logo.png')

    const login = () => {
      auth.signIn()
    }

    return {
      login,
      logoSrc
    }
  }
})
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  background-color: #2f2f2f;
}

.main-content {
  flex: 1;
  overflow: hidden;
}

:deep(.v-field__input) {
  color: white !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}
</style>
