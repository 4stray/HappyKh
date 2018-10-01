import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import ConfirmRegistration from './views/ConfirmRegistration.vue';
import Profile from './views/Profile';
import CreatePlace from './views/CreatePlace.vue';
import Auth from './components/Authentication/auth';

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
      path: '/place/create',
      name: 'createPlace',
      component: CreatePlace,
    },
  ],
});


router.beforeEach((to, from, next) => {
  Auth.checkAuthentication();
  next();
});

Vue.use(Router);


export default router;
