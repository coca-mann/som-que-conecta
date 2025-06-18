console.log("Executando router/index.js");

import { createRouter, createWebHistory } from 'vue-router'

import AccountActivationView from '../views/AccountActivationView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue')
    },
    {
      path: '/auth',
      name: 'auth',
      component: () => import('../views/AuthView.vue')
    },
    {
      path: '/activate-account/:token', // O ':token' cria um parâmetro dinâmico na URL
      name: 'AccountActivation',
      component: AccountActivationView
    },
    // --- Bloco de Artigos (Corrigido e Unificado) ---
    {
      path: '/articles',
      name: 'ArticleList',
      component: () => import('../views/ArticlesView.vue')
    },
    {
      // Rota específica de criação vem ANTES da rota dinâmica com :id
      path: '/articles/create',
      name: 'ArticleCreate',
      component: () => import('../views/ArticleCreateView.vue'),
      meta: { requiresAuth: true, requiresTeacher: true }
    },
    {
      path: '/articles/edit/:id',
      name: 'ArticleEdit',
      // Reutiliza o mesmo componente de criação, que já lida com o modo de edição
      component: () => import('../views/ArticleCreateView.vue'),
      meta: { requiresAuth: true, requiresTeacher: true }
    },
    {
      // Rota dinâmica com :id vem por último
      path: '/articles/:id',
      name: 'ArticleDetail',
      // CORREÇÃO: O nome do arquivo agora inclui "View"
      component: () => import('../views/ArticleDetail.vue'),
    },
    {
      path: '/courses',
      name: 'courses',
      component: () => import('../views/CoursesView.vue')
    },
    {
      path: '/course/:id',
      name: 'course-detail',
      component: () => import('../views/CourseDetail.vue')
    },
    {
      path: '/course/:courseId/task/:taskId',
      name: 'course-task-detail',
      component: () => import('../views/CourseTaskDetail.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/instruments',
      name: 'instruments',
      component: () => import('../views/InstrumentsView.vue'),
      // meta: { requiresAuth: true } //
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/manage-instruments',
      name: 'manage-instruments',
      component: () => import('../views/ManageInstruments.vue'),
      meta: { requiresAuth: true, requiresTeacher: true }
    },
    {
      path: "/bookings",
      name: "Bookings",
      component: () => import('../views/BookingsView.vue'),
      meta: { requiresAuth: true, requiresTeacher: true }
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('../views/ContactView.vue')
    },
    {
      path: '/help',
      name: 'help',
      component: () => import('../views/HelpCenter.vue')
    },
    {
      path: '/terms',
      name: 'terms',
      component: () => import('../views/TermsOfUse.vue')
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: () => import('../views/PrivacyPolicy.vue')
    }
  ]
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const { useAuthStore } = await import('@/stores/auth.store')
  const authStore = useAuthStore()

  const isLoggedIn = authStore.isAuthenticated
  const userRole = authStore.user?.role
  
  // 1. A rota precisa de autenticação, mas o usuário não está logado?
  if (to.meta.requiresAuth && !isLoggedIn) {
    // Redireciona para a página de login, guardando a rota que ele tentou acessar
    return next({ name: 'auth', query: { redirect: to.fullPath } })
  }

  // 2. A rota precisa de um papel de administrador/privilegiado?
  if (to.meta.requiresAdmin) {
    const privilegedRoles = ['admin', 'ong', 'professor'] // Defina os papéis privilegiados
    if (!privilegedRoles.includes(userRole)) {
      // Se o usuário não tem o papel necessário, redireciona para a home
      return next({ name: 'home' })
    }
  }

  // 3. Se passou por todas as verificações, permite o acesso
  next()
})

export default router