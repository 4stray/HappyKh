import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import ConfirmRegistration from './views/ConfirmRegistration.vue';
import RegistrationComponent from './components/RegistrationComponent.vue';
import LoginComponent from './components/LoginComponent.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,

      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      children: [
        {
          path: '/registration',
          name: 'registration',
          component: RegistrationComponent,
        },
      ]
    },

    {
      path: '/confirm_registration/:userId/:emailToken',
      name: 'confirm_registration',
      component: ConfirmRegistration,
    },
  ],
});
