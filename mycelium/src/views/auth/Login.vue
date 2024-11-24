<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-card-title class="text-center">
            <h1 class="text-h5">Login to Mycelium</h1>
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleLogin" ref="form">
              <v-text-field
                v-model="username"
                label="Username"
                prepend-icon="mdi-account"
                :rules="[v => !!v || 'Username is required']"
                required
              />
              
              <v-text-field
                v-model="password"
                label="Password"
                prepend-icon="mdi-lock"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                :type="showPassword ? 'text' : 'password'"
                @click:append="showPassword = !showPassword"
                :rules="[v => !!v || 'Password is required']"
                required
              />

              <v-text-field
                v-if="mfaRequired"
                v-model="mfaCode"
                label="MFA Code"
                prepend-icon="mdi-shield-lock"
                :rules="[v => !mfaRequired || !!v || 'MFA Code is required']"
              />

              <v-alert
                v-if="error"
                type="error"
                class="mb-4"
              >
                {{ error }}
              </v-alert>

              <v-btn
                color="primary"
                block
                type="submit"
                :loading="loading"
                class="mt-4"
              >
                Login
              </v-btn>
            </v-form>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn
              variant="text"
              to="/register"
              color="primary"
            >
              Create Account
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { useRouter } from 'vue-router'
import auth from '@/services/auth'

export default defineComponent({
  name: 'UserLogin',
  setup() {
    const router = useRouter()
    const form = ref(null)
    const loading = ref(false)
    const username = ref('')
    const password = ref('')
    const mfaCode = ref('')
    const mfaRequired = ref(false)
    const showPassword = ref(false)
    const error = ref('')

    const handleLogin = async () => {
      if (!form.value.validate()) return

      loading.value = true
      error.value = ''

      try {
        // Attempt login using AuthService
        await auth.login(username.value, password.value, mfaCode.value)
        console.log('✅ Login successful')
        router.push('/')
      } catch (err) {
        console.error('❌ Login failed:', err)
        error.value = err.response?.data?.detail || 'Login failed'
      } finally {
        loading.value = false
      }
    }

    return {
      form,
      loading,
      username,
      password,
      mfaCode,
      mfaRequired,
      showPassword,
      error,
      handleLogin
    }
  }
})
</script>
