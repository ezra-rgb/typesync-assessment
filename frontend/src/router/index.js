import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import EAS20 from '../views/EAS20.vue'
import AAS from '../views/AAS.vue'
import Results from '../views/Results.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/eas20',
    name: 'EAS20',
    component: EAS20
  },
  {
    path: '/aas',
    name: 'AAS',
    component: AAS
  },
  {
    path: '/results',
    name: 'Results',
    component: Results
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router