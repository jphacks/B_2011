import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import Store from './models/Store'
import VueNativeSock from 'vue-native-websocket'

Vue.config.productionTip = false
Vue.use(VueNativeSock, 'ws://ben.hongo.wide.ad.jp:8000', {
  connectManually: true,
})

new Vue({
  router,
  vuetify,
  store: Store,
  render: h => h(App)
}).$mount('#app')
