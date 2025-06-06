import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ArticlesView from '../views/ArticlesView.vue'
import CoursesView from '../views/CoursesView.vue'
import InstrumentsView from '../views/InstrumentsView.vue'
import ProfileView from '../views/ProfileView.vue'
import CreateArticle from '../views/CreateArticle.vue'
import ContactView from '../views/ContactView.vue'
import HelpCenterView from '../views/HelpCenter.vue'
import TermsOfUseView from '../views/TermsOfUse.vue'
import PrivacyPolicyView from '../views/PrivacyPolicy.vue'
import AuthView from '../views/AuthView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/auth',
      name: 'auth',
      component: AuthView
    },
    {
      path: '/articles',
      name: 'articles',
      component: ArticlesView
    },
    {
      path: '/article/:id',
      name: 'article-detail',
      component: () => import('../views/ArticleDetail.vue')
    },
    {
      path: '/courses',
      name: 'courses',
      component: CoursesView
    },
    {
      path: '/course/:id',
      name: 'course-detail',
      component: () => import('../views/CourseDetail.vue')
    },
    {
      path: '/course/:courseId/task/:taskId',
      name: 'course-task-detail',
      component: () => import('../views/CourseTaskDetail.vue')
    },
    {
      path: '/instruments',
      name: 'instruments',
      component: InstrumentsView
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/manage-instruments',
      name: 'manage-instruments',
      component: () => import('../views/ManageInstruments.vue')
    },
    {
      path: '/articles/create',
      name: 'create-article',
      component: CreateArticle
    },
    {
      path: '/articles/edit/:id',
      name: 'edit-article',
      component: CreateArticle
    },
    {
      path: '/contact',
      name: 'contact',
      component: ContactView
    },
    {
      path: '/help',
      name: 'help',
      component: HelpCenterView
    },
    {
      path: '/terms',
      name: 'terms',
      component: TermsOfUseView
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: PrivacyPolicyView
    }
  ]
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const isLoggedIn = false // Replace with actual auth check
  const userRole = 'student' // Replace with actual user role
  
  if (to.meta.requiresAuth && !isLoggedIn) {
    // Redirect to login or show login modal
    next('/')
  } else if (to.meta.requiresTeacher && userRole !== 'teacher' && userRole !== 'admin') {
    // Redirect if user doesn't have teacher/admin privileges
    next('/')
  } else {
    next()
  }
})

export default router