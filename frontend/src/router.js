import Vue from 'vue';
import axios from 'axios';
import Router from 'vue-router';
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import ConfirmRegistration from './views/ConfirmRegistration.vue';
import CreatePlace from './views/CreatePlace.vue';
import Profile from './views/Profile.vue';
import store from './store';


const router = new Router({
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
    },
    {
      path: '/confirm_registration/:userId/:emailToken',
      name: 'confirm_registration',
      component: ConfirmRegistration,
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
    },
    {
      path: '/places/create',
      name: 'createPlace',
      component: CreatePlace,
    },
  ],
});

router.beforeEach((to, from, next) => {
  if (store.getters.getAuthenticated) {
    const urlTokenValidation =
      'http://127.0.0.1:8000/api/users/token-validation/';

    const headers = {
      Authorization: `Token ${store.getters.getToken}`,
    };

    axios.get(
      urlTokenValidation,
      {
        headers,
      },
    ).then((response) => {
      console.log(`Token exists, status: ${response.status}`);
      next();
    }).catch((error) => {
      console.log(`Token doesn't exist, status: ${error.response.status}`);

      store.dispatch('signOut');

      next({ name: 'login' });
    });
  } else {
    console.log('executed beforeEach for a guest user');
    next();
  }
});

Vue.use(Router);

export default router;
