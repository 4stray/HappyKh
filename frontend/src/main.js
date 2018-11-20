import 'vuetify/dist/vuetify.min.css';
import 'material-design-icons-iconfont/dist/material-design-icons.css';
import Vue from 'vue';
import VueAWN from 'vue-awesome-notifications';
import VueCookies from 'vue-cookies'
import Vuetify from 'vuetify';
import './assets/styles/styles.css';
import App from './App.vue';
import router from './router';
import store from './store';

Vue.use(Vuetify);
Vue.use(VueCookies);
Vue.config.productionTip = false;
Vue.config.silent = true;

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
