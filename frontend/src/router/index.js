// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';

// Importe seus componentes de página
import HomePage from '../pages/HomePage.vue';
import ArticlePage from '../pages/ArticlePage.vue';
import InstrumentsPage from '../pages/InstrumentsPage.vue';
import InstrumentSchedulePage from '../pages/InstrumentSchedulePage.vue';
import CoursesPage from '../pages/CoursesPage.vue';
import CourseDetailPage from '../pages/CourseDetailPage.vue';
import ProfilePage from '../pages/ProfilePage.vue';
import ManageInstrumentsPage from '../pages/ManageInstrumentsPage.vue';
import ManageSchedulePage from '../pages/ManageSchedulePage.vue';
import NotFoundPage from '../pages/NotFoundPage.vue'; // Opcional

// Simulação de um store de autenticação. Em um app real, use Pinia.
// Esta função é uma forma SIMPLIFICADA de obter o estado de login para os guardas de rota.
// O estado real de isLoggedIn e userType será gerenciado no App.vue por enquanto.
const getAuthStatus = () => {
  return {
    // No App.vue, você pode atualizar o localStorage se quiser persistência simples
    // ou, idealmente, usar Pinia que é reativo e integrado.
    isLoggedIn: JSON.parse(localStorage.getItem('isLoggedIn') || 'false'),
    userType: localStorage.getItem('userType') || 'student',
  };
};


const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/artigos', name: 'Articles', component: ArticlePage },
  {
    path: '/instrumentos',
    name: 'Instruments',
    component: InstrumentsPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/instrumentos/:instrumentId/agenda',
    name: 'InstrumentSchedule',
    component: InstrumentSchedulePage,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/cursos',
    name: 'Courses',
    component: CoursesPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/cursos/:courseId',
    name: 'CourseDetail',
    component: CourseDetailPage,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/perfil',
    name: 'Profile',
    component: ProfilePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/gerenciar/instrumentos',
    name: 'ManageInstruments',
    component: ManageInstrumentsPage,
    meta: { requiresAuth: true, requiresVolunteer: true }
  },
  {
    path: '/gerenciar/agenda',
    name: 'ManageSchedule',
    component: ManageSchedulePage,
    meta: { requiresAuth: true, requiresVolunteer: true }
  },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFoundPage } // Opcional: Página 404
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0, behavior: 'smooth' };
    }
  }
});

// Guarda de Navegação (Navigation Guard)
router.beforeEach((to, from, next) => {
  const auth = getAuthStatus();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresVolunteer = to.matched.some(record => record.meta.requiresVolunteer);

  if (requiresAuth && !auth.isLoggedIn) {
    // Idealmente, aqui você dispararia um evento ou action (Pinia) para App.vue mostrar o modal de login.
    // Ou redirecionaria para uma página de login dedicada: next({ name: 'Login' });
    // Por agora, vamos permitir o acesso e a página destino pode mostrar uma mensagem de "login necessário"
    // ou o App.vue pode ter uma lógica para interceptar isso e mostrar o modal.
    // Para simplificar, a lógica de exibir o modal de login está no App.vue e as páginas
    // podem precisar de um v-if="isLoggedIn" internamente ou confiar que o App.vue tratará.
    // Para uma experiência melhor, o App.vue deveria ser notificado para abrir o modal.
    // Vamos permitir que o usuário chegue à página, e a página lida com a exibição se não logado (como no seu original)
    // Ou você pode fazer:
    // if (to.name !== 'Home') { // Evitar loop se a home for a fallback de login
    //    alert('Você precisa estar logado para acessar esta página.'); // Ou mostrar o modal
    //    return next({ name: 'Home' });
    // }
    console.warn(`Tentativa de acesso a '${to.name}' sem login.`);
    // Para este exemplo, vamos deixar App.vue gerenciar a exibição do modal quando o usuário tenta interagir
    // com algo que requer login em uma página já carregada.
    // Se a intenção é bloquear a navegação completamente, você faria `next({ name: 'Login' })` ou `next(false)`.
    next();
  } else if (requiresVolunteer && auth.userType !== 'volunteer') {
    alert('Acesso negado. Esta área é apenas para voluntários.');
    next({ name: 'Home' });
  } else {
    next();
  }
});

export default router;