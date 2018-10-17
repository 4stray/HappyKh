import Vue from 'vue';
import axios from 'axios';
import Router from 'vue-router';
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import ConfirmRegistration from './views/ConfirmRegistration.vue';
import CreatePlace from './views/CreatePlace.vue';
import Profile from './views/Profile.vue';
import store from './store';

const ifAuthenticated = (to, from, next) => {
  if (store.getters.getAuthenticated) {
    next();
  } else {
    next({ name: 'login' });
  }
};

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
      beforeEnter: ifAuthenticated,
    },
    {
      path: '/places/create',
      name: 'createPlace',
      component: CreatePlace,
      beforeEnter: ifAuthenticated,
    },
  ],
});

router.beforeEach((to, from, next) => {
  if (store.getters.getAuthenticated) {
    const urlTokenValidation =
      'http://127.0.0.1:8000/api/users/token-validation';

    const headers = {
      Authorization: `Token ${store.getters.getToken}`,
    };

    axios.get(
      urlTokenValidation,
      {
        headers,
      },
    ).then((response) => {
      next();
    }).catch((error) => {
      store.dispatch('signOut');

      next({ name: 'login' });
    });
  } else {
    next();
  }
});

Vue.use(Router);

export default router;
