import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import Store from './models/Store'

Vue.config.productionTip = false

new Vue({
  router,
  vuetify,
  store: Store,
  render: h => h(App)
}).$mount('#app')
