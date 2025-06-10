console.log("Executando router/index.js");

import { createRouter, createWebHistory } from 'vue-router'

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
      path: '/articles',
      name: 'articles',
      component: () => import('../views/ArticlesView.vue')
    },
    {
      path: '/article/:id',
      name: 'article-detail',
      component: () => import('../views/ArticleDetail.vue')
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
      meta: { requiresAuth: true }
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
      path: '/articles/create',
      name: 'create-article',
      component: () => import('../views/CreateArticle.vue'),
      meta: { requiresAuth: true, requiresTeacher: true }
    },
    {
      path: '/articles/edit/:id',
      name: 'edit-article',
      component: () => import('../views/CreateArticle.vue'),
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
  // Importamos o store AQUI DENTRO da função.
  const { useAuthStore } = await import('@/stores/auth.store')
  const authStore = useAuthStore()

  const isLoggedIn = authStore.isAuthenticated
  const userRole = authStore.user?.role // ex: 'student', 'teacher'
  
  if (to.meta.requiresAuth && !isLoggedIn) {
    // Se a rota exige login e o usuário não está logado, redireciona para o login
    next({ name: 'auth' })
  } else if (to.meta.requiresTeacher && userRole !== 'teacher' && userRole !== 'admin') {
    // Se a rota exige professor/admin e o usuário não é, redireciona para o início
    next({ name: 'home' })
  } else {
    // Em todos os outros casos, permite a navegação
    next()
  }
})

export default router