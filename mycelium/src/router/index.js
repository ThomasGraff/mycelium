import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/home/Home.vue'
import Login from '@/views/auth/Login.vue'
import Register from '@/views/auth/Register.vue'
import auth from '@/services/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresUnauth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresUnauth: false }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  // Initialize auth service if not already done
  if (!auth.isInitialized) {
    await auth.initialize();
  }

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!auth.isAuthenticated) {
      next('/login');
    } else {
      next();
    }
  } else if (to.matched.some(record => record.meta.requiresUnauth)) {
    // Redirect to home if user is already authenticated
    if (auth.isAuthenticated) {
      next('/');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router
