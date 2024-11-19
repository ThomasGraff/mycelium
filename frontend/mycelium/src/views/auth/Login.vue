<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-card-title class="text-center">
            <h1 class="text-h5">Login to Mycelium</h1>
          </v-card-title>
          <v-card-text class="text-center">
            <v-btn
              color="primary"
              size="large"
              @click="login"
              :loading="loading"
            >
              Login with Authentik
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { defineComponent, ref } from 'vue'
import auth from '@/services/auth'

export default defineComponent({
  name: 'userLogin',
  setup() {
    const loading = ref(false)

    const login = async () => {
      loading.value = true
      try {
        await auth.login()
      } catch (error) {
        console.error('❌ Login failed:', error)
      } finally {
        loading.value = false
      }
    }

    return {
      loading,
      login
    }
  }
})
</script>
