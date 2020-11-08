import Vue from 'vue'
import App from './App.vue'
import router from './router'
import "@fortawesome/fontawesome-free/css/all.css";
import "@fortawesome/fontawesome-free/js/all.js";
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

Vue.config.productionTip = false

/* 
 * Setup Buefy
 */

import Buefy from 'buefy'
import 'buefy/dist/buefy.css'

Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.use(Buefy, {
  defaultIconComponent: 'font-awesome-icon',
  defaultIconPack: 'fas',
})

new Vue({
  render: h => h(App),
  router: router,
}).$mount('#app')
