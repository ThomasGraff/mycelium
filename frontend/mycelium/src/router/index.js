import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/home/Home.vue'
import Login from '@/views/login/Login.vue'
import Register from '@/views/register/Register.vue'

// Define the routes for the application
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
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
  }
]

// Create the router instance with history mode and routes
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL), // Ensure BASE_URL is set correctly
  routes
})

export default router
