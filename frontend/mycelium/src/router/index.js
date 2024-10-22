import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/home/Home.vue'
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import mainOidc from '@/services/auth'
import Callback from '@/views/auth/Callback.vue'

// Define the routes for the application
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { authName: mainOidc.authName }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/auth/signinwin/mycelium',
    name: 'Callback',
    component: Callback
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})


mainOidc.useRouter(router)

export default router
