import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Content from '../pages/Content.vue'
import InstrumentWall from '../pages/InstrumentWall.vue'
import About from '../pages/About.vue'
import Article from '../pages/Article.vue'
import InstrumentDetail from '../pages/InstrumentDetail.vue'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Profile from '../pages/Profile.vue'
import LearningPaths from '../pages/LearningPaths.vue'
import LearningPathDetail from '../pages/LearningPathDetail.vue'
import LessonDetail from '../pages/LessonDetail.vue'

const routes = [
  { path: '/', component: Home, name: 'Home' },
  { path: '/content', component: Content, name: 'Content' },
  { path: '/instrument-wall', component: InstrumentWall, name: 'InstrumentWall' },
  { path: '/about', component: About, name: 'About' },
  { path: '/article/:id', component: Article, name: 'Article'},
  { path: '/instrument/:id', component: InstrumentDetail, name: 'InstrumentDetail'},
  { path: '/login', component: Login, name: 'Login'},
  { path: '/register', component: Register, name: 'Register'},
  { path: '/profile', component: Profile, name: 'Profile'},
  { path: '/learning', component: LearningPaths},
  { path: '/learning-path/:id', component: LearningPathDetail},
  { path: '/lesson/:id', component: LessonDetail}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
