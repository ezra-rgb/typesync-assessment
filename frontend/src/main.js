import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

// View imports
import Home from './views/Home.vue'
import Results from './views/Results.vue'

// Route definitions - 4 routes total
const routes = [
  {
    path: '/',
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
  }
]

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes
})

// Create app
const app = createApp(App)

// Use router
app.use(router)

// Mount app
app.mount('#app')