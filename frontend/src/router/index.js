import Vue from 'vue'
import Router from 'vue-router'

import Home from '@/views/Home'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/home',
      name: 'Home',
      component: Home,
    },
  ],
  linkActiveClass: 'is-active',
  linkExactActiveClass: 'is-active'
})

export default router
