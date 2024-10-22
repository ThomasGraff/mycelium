<template>
  <div>Authenticating...</div>
</template>

<script>
import { defineComponent, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import auth from '@/services/auth'

export default defineComponent({
  name: 'AuthCallback',
  setup() {
    const router = useRouter()

    onMounted(async () => {
      try {
        await auth.signinCallback()
        console.log('✅ OAuth callback success')
        router.push('/')
      } catch (error) {
        console.error('❌ OAuth callback error:', error)
        router.push('/login')
      }
    })
  }
})
</script>
