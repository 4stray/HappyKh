import Vue from 'vue';
import VueCookies from 'vue-cookies';
import App from './App.vue';
import router from './router';

import VueAWN from 'vue-awesome-notifications';

Vue.use(VueCookies);
Vue.config.productionTip = false;
const options = {
  icons: { enabled: false },
  position: 'top',
};
Vue.use(VueAWN, options);
new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
