import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '@/utils/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/manager/home' },
    {
      path: '/manager',
      name: 'Layout',
      component: () => import('@/layouts/Layout.vue'),
      children: [
        { path: 'home', name: 'Home', component: () => import('@/views/Home.vue') },
        { path: 'lab', name: 'Lab', component: () => import('@/views/Lab.vue') },
        { path: 'profile', name: 'profile', component: () => import('@/views/Profile.vue') },
        { path: 'password', name: 'password', component: () => import('@/views/Password.vue') },
        { path: 'user', name: 'User', component: () => import('@/views/User.vue') },
        { path: 'equipment', name: 'Equipment', component: () => import('@/views/Equipment.vue') },
        { path: 'lablist', name: 'LabList', component: () => import('@/views/LabList.vue') },
        {
          path: 'lab-equipment',
          name: 'LabEquipment',
          component: () => import('@/views/LabEquipment.vue')
        },
        {
          path: 'my-reservation',
          name: 'MyReservation',
          component: () => import('@/views/MyReservation.vue')
        },
        {
          path: 'audit-reservation',
          name: 'AuditReservation',
          component: () => import('@/views/AuditReservation.vue')
        },
        {
          path: 'ai-chat',
          name: 'AIChat',
          component: () => import('@/views/AIChat.vue')
        },
        {
          path: 'kb-upload',
          name: 'KbUpload',
          component: () => import('@/views/KbUpload.vue')
        }
      ]
    },
    { path: '/login', name: 'Login', component: () => import('@/views/Login.vue') },
    { path: '/register', name: 'Register', component: () => import('@/views/Register.vue') }
  ]
})

router.beforeEach((to, from) => {
  const token = getToken()
  if (to.path === '/login' || to.path === '/register') {
    return true
  } else {
    return token ? true : '/login'
  }
})

export default router
