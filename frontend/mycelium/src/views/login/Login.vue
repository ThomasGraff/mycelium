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
                <v-form ref="form" v-model="valid" lazy-validation>
                  <v-text-field
                    v-model="email"
                    :rules="emailRules"
                    label="Email"
                    required
                    prepend-icon="mdi-email"
                    color="primary"
                  ></v-text-field>
                  <v-text-field
                    v-model="password"
                    :rules="passwordRules"
                    label="Password"
                    required
                    prepend-icon="mdi-lock"
                    type="password"
                    color="primary"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-btn color="secondary" @click="goToRegister" text>Register</v-btn>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="login" :disabled="!valid">Login</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  name: 'UserLogin',
  setup () {
    const router = useRouter()
    const valid = ref(false)
    const email = ref('')
    const password = ref('')
    const logoSrc = require('@/assets/logo.png')

    const emailRules = [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
    ]

    const passwordRules = [
      v => !!v || 'Password is required',
      v => (v && v.length >= 8) || 'Password must be at least 8 characters'
    ]

    const login = () => {
      // TODO: Implement login logic
      console.log('💡 Login attempt with:', { email: email.value, password: password.value })
    }

    const goToRegister = () => {
      router.push('/register')
    }

    return {
      valid,
      email,
      password,
      emailRules,
      passwordRules,
      login,
      logoSrc,
      goToRegister
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
