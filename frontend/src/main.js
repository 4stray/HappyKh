import 'vuetify/dist/vuetify.min.css';
import Vue from 'vue';
import VueCookies from 'vue-cookies';
import VueAWN from 'vue-awesome-notifications';
import Vuetify from 'vuetify';
import App from './App.vue';
import router from './router';
import store from './store';

Vue.use(Vuetify);
Vue.use(VueCookies);
Vue.config.productionTip = false;

const options = {
  icons: { enabled: false },
  position: 'top',
};
Vue.use(VueAWN, options);

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');
