import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import ConfirmRegistration from './views/ConfirmRegistration.vue';
import CreatePlace from './views/CreatePlace.vue';
import Profile from './views/Profile.vue';
import ProfileSettings from './views/ProfileSettings.vue';
import store from './store';

const ifAuthenticated = (to, from, next) => {
  if (store.getters.getAuthenticated) {
    next();
    return;
  }
  next('/login');
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
    {
      path: '/profile/settings',
      name: 'settings',
      component: ProfileSettings,
    },
  ],
});


Vue.use(Router);

export default router;
