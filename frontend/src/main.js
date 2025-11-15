import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

// View imports
import Intro from './views/Intro.vue'
import Home from './views/Home.vue'
import Results from './views/Results.vue'
import TypeSyncSecret from './views/TypeSyncSecret.vue'

// Route definitions
const routes = [
  {
    path: '/',
    name: 'Intro',
    component: Intro
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/eas20',
    name: 'EAS20',
    component: () => import('./views/EAS20.vue')
  },
  {
    path: '/aas',
    name: 'AAS',
    component: () => import('./views/AAS.vue')
  },
  {
    path: '/results/:id',
    name: 'Results',
    component: Results
  },
  {
    path: '/typesync-secret',
    name: 'TypeSyncSecret',
    component: TypeSyncSecret
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')
