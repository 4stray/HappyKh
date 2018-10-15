import Vue from 'vue';
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

    const xhr = new XMLHttpRequest();
    xhr.open('GET', urlTokenValidation, false);
    xhr.setRequestHeader(
      'Authorization',
      `Token ${store.getters.getToken}`,
    );
    try {
      xhr.send();
    } catch (err) {

    }

    const statusCode = xhr.status;

    if (statusCode === 200) {
      console.log(`Token exists, status: ${statusCode}`);
      next();
    } else {
      console.log(`Token doesn't exist, status: ${statusCode}`);

      store.dispatch('signOut');
      store.commit('signOut');

      next('/login/');
    }
  } else {
    console.log('executed beforeEach');
    next();
  }
});

Vue.use(Router);

export default router;
