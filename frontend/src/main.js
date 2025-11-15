import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'

// View imports
import Home from './views/Home.vue'
import Results from './views/Results.vue'
import TypeSyncSecret from './views/TypeSyncSecret.vue'  // ✅ ADD THIS

// Route definitions - 5 routes total
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
  },
  {
    path: '/typesync-secret',  // ✅ ADD THIS
    name: 'TypeSyncSecret',
    component: TypeSyncSecret
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
