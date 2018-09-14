import Vue from 'vue';
import VueCookies from 'vue-cookies';
import App from './App.vue';
import router from './router';
Vue.use(VueCookies);
Vue.config.productionTip = false;

import VueAWN from "vue-awesome-notifications";
const options = {
  icons: {enabled: false},
  position: 'top center',
};
Vue.use(VueAWN, options);
new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
